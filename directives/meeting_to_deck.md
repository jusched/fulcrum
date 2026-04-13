# Meeting To Deck Directive

## Goal
Turn a meeting transcript and optional metadata into an auditable summary package that includes:
- executive summary
- 3 objectives
- 3 action items
- next steps
- risk notes
- editable deck output

## Inputs
- `inputs/meeting_transcript.txt`
- `inputs/meeting_metadata.json`
- optional audio/video file in production

## Core Workflow
1. Accept transcript-first input for the committed sample run.
2. Validate transcript presence before any model call.
3. Normalize deck content into schema-constrained JSON.
4. Validate the JSON contract before rendering.
5. Render an editable `.pptx`.
6. Pause for human review before any external distribution.

## Production Adapters
- Google Drive Trigger for intake
- OpenAI transcription for raw media
- OpenAI structured summarization for normalized JSON
- Google Slides for final publishing
- Slack for distribution notification

## Validation Rules
- exactly 3 objectives
- exactly 3 action items
- every objective/action item must include supporting evidence
- missing or malformed inputs must stop the workflow

## Failure Handling
- missing transcript: stop and report
- schema validation failure: route to manual review
- model/API failure: retry once, then route to manual review
- missing Google credentials: skip publishing branch and surface a clear warning
- deck rendering failure: preserve normalized JSON and stop with error details

## Auditability
- preserve transcript, normalized JSON, validation report, and rendered deck
- keep evidence excerpts tied to each recommendation
- document all assumptions in output artifacts

