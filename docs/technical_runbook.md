# Technical Runbook

## Purpose
Operate, troubleshoot, and extend the transcript-to-deck workflow without relying on the original builder.

## Core Paths
- `directives/meeting_to_deck.md`: workflow directive
- `inputs/`: committed sample inputs
- `schema/`: normalized JSON contract
- `execution/`: deterministic scripts
- `workflows/meeting_to_deck.json`: n8n export
- `artifacts/sample_run/`: committed sample outputs

## Environment
Create a `.env` file from `.env.example`.

Required for live model generation:
- `OPENAI_API_KEY`

Optional for production integrations:
- Google OAuth credentials
- `N8N_BASE_URL`
- Google Drive folder ID
- Google Slides template ID

## Runtime Modes
- **Sample mode:** use the committed transcript and deterministic sample content
- **Live mode:** call OpenAI for structured output generation
- **Publish mode:** optional Google Slides branch after human approval

## Operational Sequence
1. Validate transcript presence.
2. Generate or load normalized deck content JSON.
3. Validate JSON against schema.
4. Render local PPTX.
5. Pause for human review.
6. Optionally publish to Google Slides.

## Troubleshooting

### Missing transcript
- Symptom: input validation fails immediately
- Action: confirm `inputs/meeting_transcript.txt` exists and is non-empty

### Schema validation failure
- Symptom: JSON report shows missing fields or wrong counts
- Action: inspect `artifacts/sample_run/validation_report.json` and fix the upstream content generator

### OpenAI failure
- Symptom: timeout, auth error, or malformed response
- Action:
  - verify `OPENAI_API_KEY`
  - re-run in sample mode to isolate integration vs. logic failure
  - inspect the raw response before retrying

### Google publish failure
- Symptom: local PPTX succeeds but Slides branch fails
- Action:
  - verify Google credentials
  - verify presentation/template IDs
  - skip publishing and preserve the local package for manual distribution

### n8n Drive trigger confusion
- Manual executions return the latest matching event instead of behaving like an always-on workflow.
- Validate the trigger in activated mode before trusting production behavior.

## Extension Notes
- Add speaker diarization only if recordings routinely have poor attribution.
- Add support taxonomy enrichment if this expands into support automation later.
- Keep business rules outside prompts when the logic becomes stable.

## Logging Recommendations
- Store raw transcript length and file metadata.
- Log the selected runtime mode.
- Log schema validation success or failure.
- Log deck rendering success or failure.
- Capture model request IDs where available.

