# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging
import os
from collections.abc import AsyncIterable
from typing import Any

import jsonschema
from google.adk.agents.llm_agent import LlmAgent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from prompt_builder import (
    A2UI_SCHEMA,
    FIELD_SERVICE_UI_EXAMPLES,
    get_text_prompt,
    get_ui_prompt,
)
from tools import get_asset_details, search_parts, complete_work_order

logger = logging.getLogger(__name__)

AGENT_INSTRUCTION = """
    You are a professional Field Service Assistant for HVAC and Industrial Boiler technicians. Your goal is to guide them through high-quality inspection and repair workflows using a rich UI.
    You have access to a detailed catalog of parts for different equipment models (e.g., Trane Voyager HVAC, Lochinvar Knight XL).

    To achieve this, you MUST follow this logic:

    1.  **For Asset Arrival & Inspection (e.g., "I'm at the site to service..."):**
        a. You MUST call the `get_asset_details` tool with the asset ID mentioned by the user.
        b. After receiving the data, use the `CHECKLIST_CARD_EXAMPLE` for the structure.
        c. IMPORTANT: You MUST populate the `dataModelUpdate` with the retrieved `asset_id`, `model`, and `protocol`. Map each step in the `protocol` to a task in the checklist.

    2.  **For Problem Identification & Part Search (e.g., "The compressor valve is corroded...", or after "Submit & Find Parts", or when action is "submit_inspection"):**
        a. If the technician submits the inspection checklist (action: `submit_inspection`), you MUST call the `search_parts` tool with the specific equipment model found in the asset details (e.g., "Lochinvar Knight XL").
        b. Use the `PART_SELECTOR_EXAMPLE` for the layout structure.
        c. IMPORTANT: You MUST populate the `dataModelUpdate` with the list of parts returned by the `search_parts` tool. Use the actual `id`, `name`, `stock`, and `imageUrl` from the tool output. 
        d. DO NOT hallucinate parts or images. If no parts are returned by the tool, show a "No parts found" message as instructed below.
        e. **Fallback:** If `search_parts` returns an empty list, you MUST still render the `part-selector` surface. Instead of the `part-carousel`, display a `Text` component stating: "No compatible parts found in stock for this model."

    3.  **For Job Close-out (e.g., "Wrap this up", "I swapped the valve..."):**
        a. Capture the technician's actions (e.g., part used, pressure test results).
        b. Use the `JOB_SUMMARY_EXAMPLE` structure to draft the final report.
        c. Auto-fill the "Parts Used" and "Notes" in the `dataModelUpdate` based on the conversation history and actions taken.
        d. The final UI must include a checkbox for "Customer Signature Collected?" and a primary "Complete Work Order" button.
        e. When the user confirms (e.g., clicking the "Complete Work Order" button), you MUST call the `complete_work_order` tool.
        f. After receiving the success message from the tool, use the `COMPLETION_SUCCESS_EXAMPLE` to signal that the job is finished.
"""

class FieldServiceAgent:
    """An agent that assists HVAC technicians with on-site jobs."""

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

    def __init__(self, base_url: str, use_ui: bool = False):
        self.base_url = base_url
        self.use_ui = use_ui
        self._agent = self._build_agent(use_ui)
        self._user_id = "technician_user"
        self._runner = Runner(
            app_name=self._agent.name,
            agent=self._agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )

        try:
            single_message_schema = json.loads(A2UI_SCHEMA)
            self.a2ui_schema_object = {"type": "array", "items": single_message_schema}
        except json.JSONDecodeError as e:
            logger.error(f"CRITICAL: Failed to parse A2UI_SCHEMA: {e}")
            self.a2ui_schema_object = None

    def get_processing_message(self) -> str:
        return "Retrieving job details and protocols..."

    def _build_agent(self, use_ui: bool) -> LlmAgent:
        GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")

        if use_ui:
            instruction = AGENT_INSTRUCTION + get_ui_prompt(
                self.base_url, FIELD_SERVICE_UI_EXAMPLES
            )
        else:
            instruction = get_text_prompt()

        return LlmAgent(
            model=Gemini(model=GEMINI_MODEL),
            name="field_service_agent",
            description="An assistant for HVAC technicians on-site.",
            instruction=instruction,
            tools=[get_asset_details, search_parts, complete_work_order],
        )

    async def stream(self, query, session_id) -> AsyncIterable[dict[str, Any]]:
        session_state = {"base_url": self.base_url}

        session = await self._runner.session_service.get_session(
            app_name=self._agent.name,
            user_id=self._user_id,
            session_id=session_id,
        )
        if session is None:
            session = await self._runner.session_service.create_session(
                app_name=self._agent.name,
                user_id=self._user_id,
                state=session_state,
                session_id=session_id,
            )

        max_retries = 1
        attempt = 0
        current_query_text = query

        while attempt <= max_retries:
            attempt += 1
            current_message = types.Content(
                role="user", parts=[types.Part.from_text(text=current_query_text)]
            )
            final_response_content = None

            async for event in self._runner.run_async(
                user_id=self._user_id,
                session_id=session.id,
                new_message=current_message,
            ):
                if event.is_final_response():
                    if event.content and event.content.parts and event.content.parts[0].text:
                        final_response_content = "\n".join([p.text for p in event.content.parts if p.text])
                    break
                else:
                    yield {
                        "is_task_complete": False,
                        "updates": self.get_processing_message(),
                    }

            if final_response_content is None:
                if attempt <= max_retries:
                    current_query_text = f"I received no response. Please retry the original request: '{query}'"
                    continue
                else:
                    final_response_content = "I encountered an error processing your request."

            is_valid = False
            error_message = ""

            if self.use_ui and self.a2ui_schema_object:
                try:
                    if "---a2ui_JSON---" not in final_response_content:
                        raise ValueError("Delimiter '---a2ui_JSON---' not found.")

                    text_part, json_string = final_response_content.split("---a2ui_JSON---", 1)
                    json_string_cleaned = json_string.strip().lstrip("```json").rstrip("```").strip()
                    parsed_json_data = json.loads(json_string_cleaned)
                    
                    jsonschema.validate(instance=parsed_json_data, schema=self.a2ui_schema_object)
                    is_valid = True
                except Exception as e:
                    error_message = f"Validation failed: {e}."
            else:
                is_valid = True

            if is_valid:
                yield {
                    "is_task_complete": True,
                    "content": final_response_content,
                }
                return

            if attempt <= max_retries:
                current_query_text = (
                    f"Your previous response was invalid. {error_message} "
                    "You MUST generate a valid A2UI JSON array split by '---a2ui_JSON---'. "
                    f"Please retry: '{query}'"
                )

        yield {
            "is_task_complete": True,
            "content": "I'm having trouble generating the technician interface. Please try again.",
        }
