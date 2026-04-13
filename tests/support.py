from pathlib import Path


def make_valid_payload():
    return {
        "executive_summary": (
            "BrightLane should start with meeting intelligence and reporting automation "
            "before customer-facing support automation."
        ),
        "objectives": [
            {
                "title": "Prioritize an internal reporting workflow",
                "rationale": "Leadership wants time savings and better prioritization before Q4.",
                "evidence_ids": ["obj-1"],
            },
            {
                "title": "Keep customer-facing automation out of phase one",
                "rationale": "The client wants human control over customer communications.",
                "evidence_ids": ["obj-2"],
            },
            {
                "title": "Make the workflow auditable",
                "rationale": "Leaders want recommendations grounded in source material.",
                "evidence_ids": ["obj-3"],
            },
        ],
        "action_items": [
            {
                "title": "Pilot the workflow on one recurring leadership meeting",
                "owner": "Operations",
                "due_window": "Next 30 days",
                "evidence_ids": ["act-1"],
            },
            {
                "title": "Define approval before broad distribution",
                "owner": "Sarah Kim",
                "due_window": "Before launch",
                "evidence_ids": ["act-2"],
            },
            {
                "title": "Estimate monthly cost at 20 meetings",
                "owner": "AI Automation Specialist",
                "due_window": "POC review",
                "evidence_ids": ["act-3"],
            },
        ],
        "next_steps": [
            "Test the workflow on historical meeting inputs.",
            "Review deck output quality with leadership.",
            "Decide whether to add Google Slides publishing.",
        ],
        "risks": [
            "Transcript quality may degrade action-item extraction.",
            "Weak input discipline can reduce trust in the output.",
        ],
        "evidence": [
            {"id": "obj-1", "quote": "We have holiday planning starting in about three months."},
            {"id": "obj-2", "quote": "I do not want the first project to accidentally email customers the wrong thing."},
            {"id": "obj-3", "quote": "I do not want black-box outputs."},
            {"id": "act-1", "quote": "Maybe take three historical meeting recordings."},
            {"id": "act-2", "quote": "Human approval is mandatory before anything goes out broadly."},
            {"id": "act-3", "quote": "I'd also want some very basic cost estimate before we commit."},
        ],
    }


def make_metadata():
    return {
        "meeting_title": "BrightLane Retail AI Automation Discovery Call",
        "meeting_date": "2026-04-13",
        "participants": [
            "Sarah Kim",
            "Marcus Lee",
            "Tina Patel",
            "Alex Rivera",
        ],
        "review_required": True,
    }


def write_temp_transcript(temp_dir: Path) -> Path:
    path = temp_dir / "meeting_transcript.txt"
    path.write_text(
        "Sarah wants a practical phase one focused on internal reporting. "
        "Marcus wants a weekly summary with actions and trends. "
        "Tina wants future support insights but not in phase one.",
        encoding="utf-8",
    )
    return path

