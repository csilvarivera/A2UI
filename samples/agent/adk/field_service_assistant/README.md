# Field Service Assistant Sample

This sample demonstrates a Google ADK-based agent designed for HVAC technicians on-site. It uses the A2UI protocol to stream rich UI components for inspection checklists, part selection, and job close-out.

## Workflow

1.  **Smart Inspection:** The technician identifies the unit (e.g., "Roof-top Unit 4"). The agent retrieves the maintenance protocol and renders a `ChecklistCard`.
2.  **Part Identification:** The technician identifies a faulty part (e.g., "corroded compressor valve"). The agent searches for compatible parts and renders a `PartSelectorCarousel` (horizontal list).
3.  **Job Close-out:** Once repaired, the technician wraps up the job. The agent pre-fills a `JobSummaryForm` based on the conversation and prompts for completion.

## Running the Sample

To run the sample locally and see the simulated workflow:

```bash
python -m field_service_assistant
```

Note: You will need to set up your environment variables (e.g., `LITELLM_MODEL`) as with other ADK samples.
