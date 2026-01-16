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

from a2ui_examples import FIELD_SERVICE_UI_EXAMPLES

# The A2UI schema remains constant for all A2UI responses.
A2UI_SCHEMA = r'''
{
  "title": "A2UI Message Schema",
  "description": "Describes a JSON payload for an A2UI (Agent to UI) message, which is used to dynamically construct and update user interfaces. A message MUST contain exactly ONE of the action properties: 'beginRendering', 'surfaceUpdate', 'dataModelUpdate', or 'deleteSurface'.",
  "type": "object",
  "properties": {
    "beginRendering": {
      "type": "object",
      "description": "Signals the client to begin rendering a surface with a root component and specific styles.",
      "properties": {
        "surfaceId": {
          "type": "string",
          "description": "The unique identifier for the UI surface to be rendered."
        },
        "root": {
          "type": "string",
          "description": "The ID of the root component to render."
        },
        "styles": {
          "type": "object",
          "description": "Styling information for the UI.",
          "properties": {
            "font": {
              "type": "string",
              "description": "The primary font for the UI."
            },
            "primaryColor": {
              "type": "string",
              "description": "The primary UI color as a hexadecimal code (e.g., '#00BFFF').",
              "pattern": "^#[0-9a-fA-F]{6}$"
            }
          }
        }
      },
      "required": ["root", "surfaceId"]
    },
    "surfaceUpdate": {
      "type": "object",
      "description": "Updates a surface with a new set of components.",
      "properties": {
        "surfaceId": {
          "type": "string",
          "description": "The unique identifier for the UI surface to be updated."
        },
        "components": {
          "type": "array",
          "description": "A list containing all UI components for the surface.",
          "minItems": 1,
          "items": {
            "type": "object",
            "properties": {
              "id": { "type": "string" },
              "weight": { "type": "number" },
              "component": {
                "type": "object",
                "properties": {
                    "Text": { "type": "object", "properties": { "text": { "type": "object", "properties": { "literalString": { "type": "string" }, "path": { "type": "string" } } }, "usageHint": { "type": "string" } }, "required": ["text"] },
                    "Image": { "type": "object", "properties": { "url": { "type": "object", "properties": { "literalString": { "type": "string" }, "path": { "type": "string" } } }, "usageHint": { "type": "string" } }, "required": ["url"] },
                    "CheckBox": { "type": "object", "properties": { "label": { "type": "object", "properties": { "literalString": { "type": "string" }, "path": { "type": "string" } } }, "value": { "type": "object", "properties": { "literalBoolean": { "type": "boolean" }, "path": { "type": "string" } } } }, "required": ["label", "value"] },
                    "TextField": { "type": "object", "properties": { "label": { "type": "object", "properties": { "literalString": { "type": "string" }, "path": { "type": "string" } } }, "text": { "type": "object", "properties": { "literalString": { "type": "string" }, "path": { "type": "string" } } }, "textFieldType": { "type": "string" } }, "required": ["label"] },
                    "Button": { "type": "object", "properties": { "child": { "type": "string" }, "primary": { "type": "boolean" }, "action": { "type": "object", "properties": { "name": { "type": "string" }, "context": { "type": "array", "items": { "type": "object", "properties": { "key": { "type": "string" }, "value": { "type": "object" } } } } } } }, "required": ["child", "action"] },
                    "Column": { "type": "object", "properties": { "children": { "type": "object", "properties": { "explicitList": { "type": "array", "items": { "type": "string" } }, "template": { "type": "object" } } } }, "required": ["children"] },
                    "Row": { "type": "object", "properties": { "children": { "type": "object", "properties": { "explicitList": { "type": "array", "items": { "type": "string" } }, "template": { "type": "object" } } } }, "required": ["children"] },
                    "List": { "type": "object", "properties": { "direction": { "type": "string" }, "children": { "type": "object" } }, "required": ["children"] },
                    "Card": { "type": "object", "properties": { "child": { "type": "string" } }, "required": ["child"] },
                    "Divider": { "type": "object" }
                }
              }
            },
            "required": ["id", "component"]
          }
        }
      },
      "required": ["surfaceId", "components"]
    },
    "dataModelUpdate": {
      "type": "object",
      "properties": {
        "surfaceId": { "type": "string" },
        "path": { "type": "string" },
        "contents": { "type": "array", "items": { "type": "object", "properties": { "key": { "type": "string" }, "valueString": { "type": "string" }, "valueNumber": { "type": "number" }, "valueBoolean": { "type": "boolean" }, "valueMap": { "type": "array" } }, "required": ["key"] } }
      },
      "required": ["contents", "surfaceId"]
    }
  }
}
'''

def get_ui_prompt(base_url: str, examples: str) -> str:
    return f"""
    ---A2UI_SCHEMA_INSTRUCTIONS---
    You must return a valid A2UI JSON payload that strictly adheres to the following JSON schema:
    {A2UI_SCHEMA}

    ---UI_EXAMPLES---
    Here are specific examples for the Field Service Assistant:
    {examples}

    ---CORE_GENERATION_RULES---
    1.  **Strict Schema Adherence:** Your response MUST be valid JSON and MUST follow the A2UI Schema precisely.
    2.  **Delimiter Requirement:** You MUST separate your natural language explanation from the A2UI JSON with the exact string: `---a2ui_JSON---`.
    3.  **JSON Array:** The A2UI JSON part MUST be a single JSON array containing one or more A2UI messages (e.g., `beginRendering`, `surfaceUpdate`, `dataModelUpdate`).
    4.  **Static Assets:** When providing URLs for images or logos, use the base URL: {base_url} if needed.
    5.  **Data Binding:** Use `dataModelUpdate` to populate the UI with actual data retrieved from tools.
    """

def get_text_prompt() -> str:
    return "You are a helpful technician assistant. Please provide clear and concise instructions for maintenance and repair tasks."
