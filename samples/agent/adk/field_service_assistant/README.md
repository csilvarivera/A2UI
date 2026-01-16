# Field Service Assistant Sample

This sample demonstrates a Google ADK-based agent designed for HVAC technicians on-site. It uses the A2UI protocol to stream rich UI components for inspection checklists, part selection, and job close-out.

## Workflow

1.  **Smart Inspection:** The technician identifies the unit (e.g., "Roof-top Unit 4"). The agent retrieves the maintenance protocol and renders a `ChecklistCard`.
2.  **Part Identification:** The technician identifies a faulty part (e.g., "corroded compressor valve"). The agent searches for compatible parts and renders a `PartSelectorCarousel` (horizontal list).
3.  **Job Close-out:** Once repaired, the technician wraps up the job. The agent pre-fills a `JobSummaryForm` based on the conversation and prompts for completion.

## Running the Sample
1. Navigate to the samples directory:

   ```bash
   cd samples/agent/adk/field_service_assistant
   ```

2. Create an environment file with your API key:

   ```bash
   cp .env.example .env
   # Edit .env with your actual API key (do not commit .env)
   ```

3. Run an agent:

   ```bash
   uv run .
   ```

## Disclaimer

Important: The sample code provided is for demonstration purposes and illustrates the mechanics of A2UI and the Agent-to-Agent (A2A) protocol. When building production applications, it is critical to treat any agent operating outside of your direct control as a potentially untrusted entity.

All operational data received from an external agent—including its AgentCard, messages, artifacts, and task statuses—should be handled as untrusted input. For example, a malicious agent could provide crafted data in its fields (e.g., name, skills.description) that, if used without sanitization to construct prompts for a Large Language Model (LLM), could expose your application to prompt injection attacks.

Similarly, any UI definition or data stream received must be treated as untrusted. Malicious agents could attempt to spoof legitimate interfaces to deceive users (phishing), inject malicious scripts via property values (XSS), or generate excessive layout complexity to degrade client performance (DoS). If your application supports optional embedded content (such as iframes or web views), additional care must be taken to prevent exposure to malicious external sites.

Developer Responsibility: Failure to properly validate data and strictly sandbox rendered content can introduce severe vulnerabilities. Developers are responsible for implementing appropriate security measures—such as input sanitization, Content Security Policies (CSP), strict isolation for optional embedded content, and secure credential handling—to protect their systems and users.