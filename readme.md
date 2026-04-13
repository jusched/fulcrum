# FulcrumLATAM / Main Street AI Advisors - AI Engineer Test

This repo is a recruiter-readable, n8n-first take-home submission for the `AI Engineer - Test.pdf` prompt.

The solution is intentionally built to show:
- approach
- time management
- practical architecture decisions
- deterministic validation around AI output
- a minimal but real proof of concept

The core flow is:

`meeting transcript -> structured JSON -> validation -> editable PPTX deck`

For the committed proof of concept, the pipeline is `transcript-first`.
For the documented production path, the same normalized JSON contract can be fed by:
- Google Drive intake
- transcription from meeting media
- OpenAI structured summarization
- Google Slides publishing
- Slack notification

## What The Submission Covers

This repo maps directly to the four parts requested in the PDF.

### Part 1: Solution Architecture
- [docs/architecture.md](C:/Users/juans/Desktop/tech/fulcrum/docs/architecture.md)
- Includes system components, integration points, data flow, validation gates, failure handling, and a `mermaid` workflow diagram.

### Part 2: Technology Cost Estimate
- [docs/cost_estimate.md](C:/Users/juans/Desktop/tech/fulcrum/docs/cost_estimate.md)
- Includes assumptions, recurring cost scenarios, and variable cost notes.

### Part 3: Functional Build (POC)
- [execution/build_sample_package.py](C:/Users/juans/Desktop/tech/fulcrum/execution/build_sample_package.py)
- [execution/render_pptx.py](C:/Users/juans/Desktop/tech/fulcrum/execution/render_pptx.py)
- [execution/validate_deck_content.py](C:/Users/juans/Desktop/tech/fulcrum/execution/validate_deck_content.py)
- [workflows/meeting_to_deck.json](C:/Users/juans/Desktop/tech/fulcrum/workflows/meeting_to_deck.json)
- [artifacts/sample_run/deck_content.json](C:/Users/juans/Desktop/tech/fulcrum/artifacts/sample_run/deck_content.json)
- [artifacts/sample_run/meeting_deck.pptx](C:/Users/juans/Desktop/tech/fulcrum/artifacts/sample_run/meeting_deck.pptx)

### Part 4: Documentation (Dual Audience)
- Non-technical: [docs/client_brief.md](C:/Users/juans/Desktop/tech/fulcrum/docs/client_brief.md)
- Technical: [docs/technical_runbook.md](C:/Users/juans/Desktop/tech/fulcrum/docs/technical_runbook.md)

## Submission Strategy

The recruiter explicitly said the focus is `approach and time management`.

Because of that, this repo was optimized for:
- fast human review first
- runnable proof second
- honest production path third

That means:
- the repo is understandable without running anything
- the sample outputs are already committed
- the proof of concept works locally without Google OAuth
- production integrations are shown clearly, but not faked

## Repository Map

### Inputs
- [inputs/meeting_transcript.txt](C:/Users/juans/Desktop/tech/fulcrum/inputs/meeting_transcript.txt): committed source transcript used for the sample run
- [inputs/meeting_metadata.json](C:/Users/juans/Desktop/tech/fulcrum/inputs/meeting_metadata.json): meeting metadata used in rendering and packaging

### Directive
- [directives/meeting_to_deck.md](C:/Users/juans/Desktop/tech/fulcrum/directives/meeting_to_deck.md): operating directive for the workflow

### Execution Layer
- [execution/build_sample_package.py](C:/Users/juans/Desktop/tech/fulcrum/execution/build_sample_package.py): orchestrates the local package build
- [execution/validate_deck_content.py](C:/Users/juans/Desktop/tech/fulcrum/execution/validate_deck_content.py): validates output JSON against schema and evidence linkage
- [execution/render_pptx.py](C:/Users/juans/Desktop/tech/fulcrum/execution/render_pptx.py): renders the editable PowerPoint deck

### Schema
- [schema/deck_content.schema.json](C:/Users/juans/Desktop/tech/fulcrum/schema/deck_content.schema.json): strict normalized data contract

### Tests
- [tests/test_validate_deck_content.py](C:/Users/juans/Desktop/tech/fulcrum/tests/test_validate_deck_content.py)
- [tests/test_render_pptx.py](C:/Users/juans/Desktop/tech/fulcrum/tests/test_render_pptx.py)
- [tests/test_build_sample_package.py](C:/Users/juans/Desktop/tech/fulcrum/tests/test_build_sample_package.py)
- [tests/support.py](C:/Users/juans/Desktop/tech/fulcrum/tests/support.py)

### Workflow
- [workflows/meeting_to_deck.json](C:/Users/juans/Desktop/tech/fulcrum/workflows/meeting_to_deck.json): n8n workflow export for the POC and production adapters

### Generated Artifacts
- [artifacts/sample_run/deck_content.json](C:/Users/juans/Desktop/tech/fulcrum/artifacts/sample_run/deck_content.json): normalized deck payload
- [artifacts/sample_run/validation_report.json](C:/Users/juans/Desktop/tech/fulcrum/artifacts/sample_run/validation_report.json): validation result proving schema compliance
- [artifacts/sample_run/executive_summary.md](C:/Users/juans/Desktop/tech/fulcrum/artifacts/sample_run/executive_summary.md): readable summary output
- [artifacts/sample_run/meeting_deck.pptx](C:/Users/juans/Desktop/tech/fulcrum/artifacts/sample_run/meeting_deck.pptx): editable deck artifact

### Supporting Docs
- [docs/architecture.md](C:/Users/juans/Desktop/tech/fulcrum/docs/architecture.md)
- [docs/cost_estimate.md](C:/Users/juans/Desktop/tech/fulcrum/docs/cost_estimate.md)
- [docs/client_brief.md](C:/Users/juans/Desktop/tech/fulcrum/docs/client_brief.md)
- [docs/technical_runbook.md](C:/Users/juans/Desktop/tech/fulcrum/docs/technical_runbook.md)
- [docs/time_management.md](C:/Users/juans/Desktop/tech/fulcrum/docs/time_management.md)

## Data Contract

The normalized output format is enforced before deck rendering.

Required fields:
- `executive_summary`
- `objectives` with exactly 3 items
- `action_items` with exactly 3 items
- `next_steps`
- `risks`
- `evidence`

Additional rule:
- each objective and each action item must reference evidence IDs that actually exist

This is the key engineering choice in the submission:
AI output is not trusted directly. It is normalized and validated before being used.

## How To Run The Local POC

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the tests:

```powershell
python -m unittest discover -s tests -v
```

Generate the sample package:

```powershell
python -m execution.build_sample_package --mode sample
```

That command writes outputs into:
- [artifacts/sample_run](C:/Users/juans/Desktop/tech/fulcrum/artifacts/sample_run)

## Runtime Modes

### `sample`
- deterministic
- does not require an API key
- uses transcript-first local packaging
- exists to make the take-home reviewable and runnable

### `live`
- intended for real OpenAI structured output generation
- requires `OPENAI_API_KEY`
- keeps the same schema and validation layer

## Environment Variables

See:
- [\.env.example](C:/Users/juans/Desktop/tech/fulcrum/.env.example)

Important keys:
- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`
- `N8N_BASE_URL`
- `USE_TRANSCRIPT_INPUT`
- `PUBLISH_TO_GOOGLE_SLIDES`
- Google credential placeholders for future publishing

## Why n8n Is Included

The prompt is about AI automation and orchestration, not only Python scripting.

So the design uses:
- Python for deterministic execution and validation
- n8n for legible orchestration and integration surface

This is deliberate:
- reviewers can inspect the workflow visually
- the reliable logic stays in code and tests
- production adapters are explicit instead of implied

## What Is Real Today

Implemented and verified:
- transcript input in repo
- metadata input in repo
- strict schema contract
- schema validation
- evidence reference validation
- editable PowerPoint generation
- sample output package generation
- automated tests covering contract and artifact generation
- n8n workflow export showing the orchestration path

## What Is Documented But Not Activated

These are present as the production path, but intentionally not activated in the committed POC:
- Google Drive trigger intake
- Google Slides publishing
- Slack notification
- live OpenAI generation in the submitted sample artifacts

Reason:
- no credentials are committed
- the goal was to avoid a fake "fully integrated" submission that cannot be reviewed safely

## Risks And Tradeoffs

- The POC is transcript-first, not media-first.
- The live model path exists in code but was not used for the committed artifact generation because no API key was available in the environment.
- The Google Slides branch is documented and represented in n8n, but local PPTX is the proof target because it is inspectable offline.
- Styling is intentionally simple. The test is about workflow quality, not presentation design.

## Verification Status

Verified during implementation:

```powershell
python -m unittest discover -s tests -v
python -m execution.build_sample_package --mode sample
```

Observed result:
- tests passed
- sample artifact package was generated
- validation report returned `valid: true`

## Recommended Review Order

If you are evaluating the submission quickly, read in this order:

1. [readme.md](C:/Users/juans/Desktop/tech/fulcrum/readme.md)
2. [docs/architecture.md](C:/Users/juans/Desktop/tech/fulcrum/docs/architecture.md)
3. [docs/cost_estimate.md](C:/Users/juans/Desktop/tech/fulcrum/docs/cost_estimate.md)
4. [artifacts/sample_run/executive_summary.md](C:/Users/juans/Desktop/tech/fulcrum/artifacts/sample_run/executive_summary.md)
5. [artifacts/sample_run/meeting_deck.pptx](C:/Users/juans/Desktop/tech/fulcrum/artifacts/sample_run/meeting_deck.pptx)
6. [workflows/meeting_to_deck.json](C:/Users/juans/Desktop/tech/fulcrum/workflows/meeting_to_deck.json)

## Final Positioning

This submission does not try to look bigger than it is.

It is a narrow, testable, auditable workflow package that shows:
- how the system would work
- where human review belongs
- how AI output is controlled
- how the solution could move from a local proof of concept to an operational workflow

That is the intended response to the take-home prompt.
