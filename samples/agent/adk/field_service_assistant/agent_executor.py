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

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import (
    DataPart,
    Part,
    Task,
    TaskState,
    TextPart,
    UnsupportedOperationError,
)
from a2a.utils import (
    new_agent_parts_message,
    new_agent_text_message,
    new_task,
)
from a2a.utils.errors import ServerError
from a2ui.a2ui_extension import create_a2ui_part, try_activate_a2ui_extension
from agent import FieldServiceAgent

logger = logging.getLogger(__name__)

class FieldServiceAgentExecutor(AgentExecutor):
    """Field Service AgentExecutor."""

    def __init__(self, base_url: str):
        self.ui_agent = FieldServiceAgent(base_url=base_url, use_ui=True)
        self.text_agent = FieldServiceAgent(base_url=base_url, use_ui=False)

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        query = ""
        ui_event_part = None
        action = None

        logger.info(
            f"--- Client requested extensions: {context.requested_extensions} ---"
        )
        use_ui = try_activate_a2ui_extension(context)

        if use_ui:
            agent = self.ui_agent
            logger.info("--- AGENT_EXECUTOR: A2UI extension active. ---")
        else:
            agent = self.text_agent
            logger.info("--- AGENT_EXECUTOR: A2UI extension not active. ---")

        if context.message and context.message.parts:
            for part in context.message.parts:
                if isinstance(part.root, DataPart):
                    if "userAction" in part.root.data:
                        ui_event_part = part.root.data["userAction"]
                    elif "ClientEvent" in part.root.data:
                         # Handle direct ClientEvent if needed
                         ui_event_part = part.root.data["ClientEvent"]

        if ui_event_part:
            logger.info(f"Received a2ui ClientEvent: {ui_event_part}")
            action = ui_event_part.get("name")
            ctx = ui_event_part.get("context", {})

            if action == "identify_part":
                model = ctx.get("model", "the current equipment")
                query = f"The technician needs to search for compatible parts for {model}."
            elif action == "submit_inspection":
                model = ctx.get("model", "the current equipment")
                query = f"The technician has completed the inspection checklist for {model} and needs to find replacement parts for any failed items."
            elif action == "complete_work_order":
                parts = ctx.get("parts_used", "None")
                notes = ctx.get("notes", "None")
                signed = ctx.get("signed", False)  # Fixed key name to match example
                query = f"User is completing the work order for {ctx.get('model', 'the asset')}. Parts used: {parts}. Notes: {notes}. Signed: {signed}."
            else:
                query = f"User performed action: {action} with context: {ctx}"
        else:
            query = context.get_user_input()

        logger.info(f"--- AGENT_EXECUTOR: Final query: '{query}' ---")

        task = context.current_task
        if not task:
            task = new_task(context.message)
            await event_queue.enqueue_event(task)
        updater = TaskUpdater(event_queue, task.id, task.context_id)

        async for item in agent.stream(query, task.context_id):
            is_task_complete = item["is_task_complete"]
            if not is_task_complete:
                await updater.update_status(
                    TaskState.working,
                    new_agent_text_message(item["updates"], task.context_id, task.id),
                )
                continue

            content = item["content"]
            final_parts = []
            if "---a2ui_JSON---" in content:
                text_content, json_string = content.split("---a2ui_JSON---", 1)

                if text_content.strip():
                    final_parts.append(Part(root=TextPart(text=text_content.strip())))

                if json_string.strip():
                    try:
                        json_string_cleaned = json_string.strip().lstrip("```json").rstrip("```").strip()
                        json_data = json.loads(json_string_cleaned)

                        if isinstance(json_data, list):
                            for message in json_data:
                                final_parts.append(create_a2ui_part(message))
                        else:
                            final_parts.append(create_a2ui_part(json_data))

                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse UI JSON: {e}")
                        final_parts.append(Part(root=TextPart(text=json_string)))
            else:
                final_parts.append(Part(root=TextPart(text=content.strip())))

            await updater.update_status(
                TaskState.input_required,
                new_agent_parts_message(final_parts, task.context_id, task.id),
                final=False,
            )
            break

    async def cancel(
        self, request: RequestContext, event_queue: EventQueue
    ) -> Task | None:
        raise ServerError(error=UnsupportedOperationError())
