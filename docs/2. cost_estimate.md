# Technology Cost Estimate

## Assumptions
- 20 meetings per month
- Average meeting length: 45 minutes
- Transcript-first proof of concept; transcription cost shown for production
- Rough text volume per meeting:
  - 18,000 input tokens for transcript + prompt context
  - 1,500 output tokens for structured summary + deck payload
- Google Workspace already exists

## Option A: Lean Production
Best when the team wants the lowest recurring cost and can self-host n8n.

| Cost Item | Assumption | Monthly Estimate |
| --- | --- | ---: |
| n8n Community Edition | Self-hosted | $0 software license |
| Small VM / container host | Basic always-on instance | $15-$30 |
| OpenAI structured output | 360k input + 30k output tokens via `gpt-4o-mini` | ~$0.07 |
| OpenAI transcription | 900 audio minutes via `gpt-4o-mini-transcribe` | ~$1.70 |
| Google Drive / Slides API | Existing Workspace | $0 incremental |
| Slack notification | Existing workspace | $0 incremental |
| **Estimated monthly total** |  | **~$17-$32** |

## Option B: Managed Production
Best when the team prefers hosted orchestration and less operational overhead.

| Cost Item | Assumption | Monthly Estimate |
| --- | --- | ---: |
| n8n Cloud Starter | Official entry tier | ~EUR 20 |
| OpenAI structured output | Same usage as above | ~$0.07 |
| OpenAI transcription | Same usage as above | ~$1.70 |
| Google Drive / Slides API | Existing Workspace | $0 incremental |
| Slack notification | Existing workspace | $0 incremental |
| **Estimated monthly total** |  | **~EUR 20 + $1.77** |

## Option C: Managed Production With Growth Buffer
Useful if the workflow expands beyond one recurring meeting stream.

| Cost Item | Assumption | Monthly Estimate |
| --- | --- | ---: |
| n8n Cloud Pro | Official team tier | ~EUR 50 |
| OpenAI structured output | 60 meetings instead of 20 | ~$0.22 |
| OpenAI transcription | 2,700 audio minutes | ~$5.10 |
| Google Drive / Slides API | Existing Workspace | $0 incremental |
| Slack notification | Existing workspace | $0 incremental |
| **Estimated monthly total** |  | **~EUR 50 + $5.32** |

## Notes
- The dominant recurring cost is orchestration hosting, not the model call itself.
- Google Slides publishing does not materially change the monthly estimate unless a custom template process is added.
- Human review time is intentionally not removed from the workflow because that is part of the risk control.
- If recordings are inconsistent or low quality, transcription cleanup can become a larger operational cost than API usage.
