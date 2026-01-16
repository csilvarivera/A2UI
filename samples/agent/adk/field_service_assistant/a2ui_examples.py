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

FIELD_SERVICE_UI_EXAMPLES = """
---BEGIN CHECKLIST_CARD_EXAMPLE---
[
  {{ "beginRendering": {{ "surfaceId": "checklist", "root": "checklist-card", "styles": {{ "primaryColor": "#4F46E5", "font": "Outfit" }} }} }},
  {{ "surfaceUpdate": {{
    "surfaceId": "checklist",
    "components": [
      {{ "id": "checklist-card", "component": {{ "Card": {{ "child": "checklist-column" }} }} }},
      {{ "id": "checklist-column", "component": {{ "Column": {{ "children": {{ "explicitList": ["checklist-title", "asset-info", "task-list", "submit-button"] }} }} }} }},
      {{ "id": "checklist-title", "component": {{ "Text": {{ "usageHint": "h2", "text": {{ "literalString": "Smart Inspection Checklist" }} }} }} }},
      {{ "id": "asset-info", "component": {{ "Text": {{ "usageHint": "caption", "text": {{ "path": "assetName" }} }} }} }},
      {{ "id": "task-list", "component": {{ "Column": {{ "children": {{ "template": {{ "componentId": "task-item-template", "dataBinding": "/tasks" }} }} }} }} }},
      {{ "id": "task-item-template", "component": {{ "CheckBox": {{ "label": {{ "path": "taskName" }}, "value": {{ "path": "completed" }} }} }} }},
      {{ "id": "submit-button", "component": {{ "Button": {{ "child": "submit-text", "primary": true, "action": {{ "name": "submit_inspection", "context": [ {{ "key": "model", "value": {{ "path": "assetModel" }} }} ] }} }} }} }},
      {{ "id": "submit-text", "component": {{ "Text": {{ "text": {{ "literalString": "Submit & Find Parts" }} }} }} }}
    ]
  }} }},
  {{ "dataModelUpdate": {{
    "surfaceId": "checklist",
    "path": "/",
    "contents": [
      {{ "key": "assetName", "valueString": "[Asset Name] ([Asset Model])" }},
      {{ "key": "tasks", "valueMap": [
        {{ "key": "task1", "valueMap": [ {{ "key": "taskName", "valueString": "[Task 1]" }}, {{ "key": "completed", "valueBoolean": false }} ] }},
        {{ "key": "task2", "valueMap": [ {{ "key": "taskName", "valueString": "[Task 2]" }}, {{ "key": "completed", "valueBoolean": false }} ] }}
      ] }}
    ]
  }} }}
]
---END CHECKLIST_CARD_EXAMPLE---

---BEGIN PART_SELECTOR_EXAMPLE---
[
  {{ "beginRendering": {{ "surfaceId": "part-selector", "root": "selector-column", "styles": {{ "primaryColor": "#4F46E5", "font": "Outfit" }} }} }},
  {{ "surfaceUpdate": {{
    "surfaceId": "part-selector",
    "components": [
      {{ "id": "selector-column", "component": {{ "Column": {{ "children": {{ "explicitList": ["selector-title", "part-carousel"] }} }} }} }},
      {{ "id": "selector-title", "component": {{ "Text": {{ "usageHint": "h2", "text": {{ "literalString": "Identify Compatible Parts" }} }} }} }},
      {{ "id": "part-carousel", "component": {{ "List": {{ "direction": "horizontal", "children": {{ "template": {{ "componentId": "part-card-template", "dataBinding": "/parts" }} }} }} }} }},
      {{ "id": "part-card-template", "component": {{ "Card": {{ "child": "part-card-layout" }} }} }},
      {{ "id": "part-card-layout", "component": {{ "Column": {{ "children": {{ "explicitList": ["part-image", "part-name", "part-stock", "select-button"] }} }} }} }},
      {{ "id": "part-image", "component": {{ "Image": {{ "url": {{ "path": "imageUrl" }}, "usageHint": "mediumFeature" }} }} }},
      {{ "id": "part-name", "component": {{ "Text": {{ "usageHint": "h4", "text": {{ "path": "name" }} }} }} }},
      {{ "id": "part-stock", "component": {{ "Text": {{ "usageHint": "caption", "text": {{ "path": "stock" }} }} }} }},
      {{ "id": "select-button", "component": {{ "Button": {{ "child": "select-text", "primary": true, "action": {{ "name": "select_part", "context": [ {{ "key": "partId", "value": {{ "path": "id" }} }}, {{ "key": "partName", "value": {{ "path": "name" }} }} ] }} }} }} }},
      {{ "id": "select-text", "component": {{ "Text": {{ "text": {{ "literalString": "Select" }} }} }} }}
    ]
  }} }},
  {{ "dataModelUpdate": {{
    "surfaceId": "part-selector",
    "path": "/",
    "contents": [
      {{ "key": "parts", "valueMap": [
        {{ "key": "part1", "valueMap": [
          {{ "key": "id", "valueString": "[Part ID]" }},
          {{ "key": "name", "valueString": "[Part Name]" }},
          {{ "key": "stock", "valueString": "[Stock Status]" }},
          {{ "key": "imageUrl", "valueString": "[Image URL]" }}
        ] }}
      ] }}
    ]
  }} }}
]
---END PART_SELECTOR_EXAMPLE---

---BEGIN JOB_SUMMARY_EXAMPLE---
[
  {{ "beginRendering": {{ "surfaceId": "job-summary", "root": "summary-column", "styles": {{ "primaryColor": "#4F46E5", "font": "Outfit" }} }} }},
  {{ "surfaceUpdate": {{
    "surfaceId": "job-summary",
    "components": [
      {{ "id": "summary-column", "component": {{ "Column": {{ "children": {{ "explicitList": ["summary-title", "parts-used-field", "notes-field", "signature-checkbox", "complete-button"] }} }} }} }},
      {{ "id": "summary-title", "component": {{ "Text": {{ "usageHint": "h2", "text": {{ "literalString": "Job Close-out" }} }} }} }},
      {{ "id": "parts-used-field", "component": {{ "TextField": {{ "label": {{ "literalString": "Parts Used" }}, "text": {{ "path": "partsUsed" }} }} }} }},
      {{ "id": "notes-field", "component": {{ "TextField": {{ "label": {{ "literalString": "Notes" }}, "text": {{ "path": "notes" }}, "textFieldType": "longText" }} }} }},
      {{ "id": "signature-checkbox", "component": {{ "CheckBox": {{ "label": {{ "literalString": "Customer Signature Collected?" }}, "value": {{ "path": "signed" }} }} }} }},
      {{ "id": "complete-button", "component": {{ "Button": {{ "child": "complete-text", "primary": true, "action": {{ "name": "complete_work_order", "context": [ {{ "key": "partsUsed", "value": {{ "path": "partsUsed" }} }}, {{ "key": "notes", "value": {{ "path": "notes" }} }}, {{ "key": "signed", "value": {{ "path": "signed" }} }} ] }} }} }} }},
      {{ "id": "complete-text", "component": {{ "Text": {{ "text": {{ "literalString": "Complete Work Order" }} }} }} }}
    ]
  }} }},
  {{ "dataModelUpdate": {{
    "surfaceId": "job-summary",
    "path": "/",
    "contents": [
      {{ "key": "partsUsed", "valueString": "[Parts Summary]" }},
      {{ "key": "notes", "valueString": "[Technician Notes]" }},
      {{ "key": "signed", "valueBoolean": false }}
    ]
  }} }}
]
---END JOB_SUMMARY_EXAMPLE---

---BEGIN COMPLETION_SUCCESS_EXAMPLE---
[
  {{ "beginRendering": {{ "surfaceId": "completion-success", "root": "success-column", "styles": {{ "primaryColor": "#10B981", "font": "Outfit" }} }} }},
  {{ "surfaceUpdate": {{
    "surfaceId": "completion-success",
    "components": [
      {{ "id": "success-column", "component": {{ "Column": {{ "children": {{ "explicitList": ["success-icon", "success-title", "success-msg", "home-button"] }} }} }} }},
      {{ "id": "success-icon", "component": {{ "Text": {{ "usageHint": "h1", "text": {{ "literalString": "✅" }} }} }} }},
      {{ "id": "success-title", "component": {{ "Text": {{ "usageHint": "h2", "text": {{ "literalString": "Work Order Complete" }} }} }} }},
      {{ "id": "success-msg", "component": {{ "Text": {{ "usageHint": "body", "text": {{ "literalString": "The report has been submitted and the job is now closed." }} }} }} }},
      {{ "id": "home-button", "component": {{ "Button": {{ "child": "home-text", "primary": true, "action": {{ "name": "go_home" }} }} }} }},
      {{ "id": "home-text", "component": {{ "Text": {{ "text": {{ "literalString": "Return to Dashboard" }} }} }} }}
    ]
  }} }}
]
---END COMPLETION_SUCCESS_EXAMPLE---
"""
