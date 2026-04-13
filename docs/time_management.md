# Time Management And Delivery Strategy

## What The Recruiter Is Actually Testing
This take-home is not asking for a production system in two hours. It is testing whether the work is scoped rationally, whether tradeoffs are explicit, and whether the deliverable is useful before it is complete.

## Delivery Strategy
I optimized for:
- reviewability first
- runnable proof second
- production realism without fake completeness

That means:
- the repo is readable without running anything
- the sample outputs are committed
- the workflow path is concrete
- the live integrations are documented honestly where credentials are unavailable

## Planned 2-Hour Allocation
- **0:00-0:20** Understand the prompt, inspect provided artifacts, define assumptions
- **0:20-0:45** Produce architecture and workflow decisions
- **0:45-1:10** Lock the JSON contract and cost model
- **1:10-1:40** Build the runnable proof of concept and export the workflow
- **1:40-2:00** Polish README, package artifacts, list risks and next steps

## Why This Allocation Works
- It protects the highest-signal items first: architecture, assumptions, and operating logic.
- It prevents spending the whole exercise on OAuth or deck styling.
- It leaves enough time to verify outputs and explain limitations clearly.

## Deliberate Non-Goals
- No attempt to fake a fully automated Google-native deployment without credentials
- No unnecessary frontend or dashboard layer
- No over-engineered agent system when a structured workflow is enough

## What Good Looks Like At The End
- A reviewer can understand the solution in under five minutes.
- The repo contains a credible workflow, not just diagrams.
- The sample output looks grounded in the transcript.
- The limitations are explicit, not hidden.

