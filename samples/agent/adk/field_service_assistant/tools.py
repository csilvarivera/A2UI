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
import os
from typing import Any, Dict, List

def _load_data():
    data_path = os.path.join(os.path.dirname(__file__), "field_service_data.json")
    with open(data_path, "r") as f:
        return json.load(f)

def get_asset_details(asset_id: str) -> Dict[str, Any]:
    """
    Looks up details for a specific asset (e.g., 'Roof-top Unit 4').
    
    Args:
        asset_id: The ID or name of the asset.
        
    Returns:
        A dictionary containing the asset model and maintenance protocol.
    """
    data = _load_data()
    asset = data["assets"].get(asset_id)
    if asset:
        return {"asset_id": asset_id, **asset}
    return {"error": f"Asset '{asset_id}' not found."}

def search_parts(asset_model: str) -> List[Dict[str, Any]]:
    """
    Searches for compatible parts for a given asset model.
    
    Args:
        asset_model: The model of the asset (e.g., 'Trane Voyager HVAC').
        
    Returns:
        A list of compatible parts with stock information.
    """
    data = _load_data()
    # Filter parts that match the asset model (simple string containment for flexibility)
    return [
        part for part in data.get("parts", [])
        if part.get("model", "").lower() in asset_model.lower() or asset_model.lower() in part.get("model", "").lower()
    ]

def complete_work_order(parts_used: str, notes: str, customer_signed: bool) -> str:
    """
    Finalizes the work order and generates a report summary.
    
    Args:
        parts_used: Description of parts used (e.g., '1x Standard Brass Valve').
        notes: Technician's notes on the work performed.
        customer_signed: Whether the customer signature was collected.
        
    Returns:
        A confirmation message that the work order has been completed.
    """
    return f"Work Order Completed successfully. Parts: {parts_used}. Notes: {notes}. Signature: {'Collected' if customer_signed else 'Missing'}."
