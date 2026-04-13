from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

import requests

from execution.render_pptx import render_presentation
from execution.validate_deck_content import load_schema, validate_file, validate_payload


REPO_ROOT = Path(__file__).resolve().parent.parent


def _read_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def _sanitize_text(text: str) -> str:
    cleaned = text.replace("\u0019", "'").replace("\u0013", "-")
    return re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", " ", cleaned)


def _read_text(path: str | Path) -> str:
    raw_text = Path(path).read_text(encoding="utf-8")
    return _sanitize_text(raw_text).strip()


def _split_sentences(transcript: str) -> list[str]:
    cleaned = transcript.replace("\n", " ")
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", cleaned) if part.strip()]


def _find_sentence(transcript: str, keyword: str, fallback: str) -> str:
    for sentence in _split_sentences(transcript):
        if keyword.lower() in sentence.lower():
            return sentence
    return fallback


def _build_sample_payload(transcript: str) -> dict[str, Any]:
    return {
        "executive_summary": (
            "BrightLane should start with an internal meeting intelligence workflow that turns "
            "leadership calls into a reviewed summary package before expanding into customer-facing automation."
        ),
        "objectives": [
            {
                "title": "Automate recurring internal reporting first",
                "rationale": (
                    "The highest-confidence phase-one value is reducing manual weekly reporting "
                    "work before holiday planning."
                ),
                "evidence_ids": ["obj-1"],
            },
            {
                "title": "Keep human review for all distributed outputs",
                "rationale": (
                    "Leadership wants time savings, but not black-box or uncontrolled messaging."
                ),
                "evidence_ids": ["obj-2"],
            },
            {
                "title": "Use auditable AI plus deterministic rules",
                "rationale": (
                    "The workflow should synthesize what matters while preserving traceability to source evidence."
                ),
                "evidence_ids": ["obj-3"],
            },
        ],
        "action_items": [
            {
                "title": "Pilot the workflow on one recurring leadership meeting type",
                "owner": "Marcus Lee",
                "due_window": "Before holiday planning",
                "evidence_ids": ["act-1"],
            },
            {
                "title": "Add an approval step before Slack or Slide distribution",
                "owner": "Sarah Kim",
                "due_window": "Phase one launch",
                "evidence_ids": ["act-2"],
            },
            {
                "title": "Prepare a rough monthly cost view for 20 meetings",
                "owner": "AI Automation Specialist",
                "due_window": "POC review",
                "evidence_ids": ["act-3"],
            },
        ],
        "next_steps": [
            "Run the workflow against three historical meeting transcripts.",
            "Review objective/action quality with operations leadership.",
            "Decide whether to enable Google Slides publishing after review.",
        ],
        "risks": [
            "Transcript quality can weaken action-item extraction and evidence mapping.",
            "Inconsistent input discipline will reduce trust in the output package.",
        ],
        "evidence": [
            {
                "id": "obj-1",
                "quote": _find_sentence(
                    transcript,
                    "holiday planning",
                    "We have holiday planning starting in about three months.",
                ),
            },
            {
                "id": "obj-2",
                "quote": _find_sentence(
                    transcript,
                    "human approval is mandatory",
                    "Human approval is mandatory before anything goes out broadly.",
                ),
            },
            {
                "id": "obj-3",
                "quote": _find_sentence(
                    transcript,
                    "black-box outputs",
                    "I do not want black-box outputs.",
                ),
            },
            {
                "id": "act-1",
                "quote": _find_sentence(
                    transcript,
                    "one recurring meeting",
                    "Maybe take three historical meeting recordings and test how well the workflow performs.",
                ),
            },
            {
                "id": "act-2",
                "quote": _find_sentence(
                    transcript,
                    "mandatory before anything goes out broadly",
                    "At least initially, human approval is mandatory before anything goes out broadly.",
                ),
            },
            {
                "id": "act-3",
                "quote": _find_sentence(
                    transcript,
                    "cost estimate",
                    "I'd also want some very basic cost estimate before we commit.",
                ),
            },
        ],
    }


def _build_live_payload(transcript: str, metadata: dict[str, Any]) -> dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for live mode.")

    schema = load_schema()
    prompt = (
        "You are building a meeting-to-deck payload. Return only schema-compliant JSON with "
        "exactly 3 objectives and 3 action items. Ground every recommendation in transcript evidence.\n\n"
        f"Meeting metadata:\n{json.dumps(metadata, indent=2)}\n\nTranscript:\n{transcript}"
    )
    response = requests.post(
        f"{os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1').rstrip('/')}/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "Return grounded deck content JSON only.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "deck_content",
                    "strict": True,
                    "schema": schema,
                },
            },
        },
        timeout=60,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    return json.loads(content)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


def _write_markdown_summary(path: Path, payload: dict[str, Any], metadata: dict[str, Any], mode: str) -> None:
    lines = [
        f"# {metadata['meeting_title']}",
        "",
        f"Mode: `{mode}`",
        "",
        "## Executive Summary",
        payload["executive_summary"],
        "",
        "## Objectives",
    ]
    lines.extend(
        [f"- **{item['title']}**: {item['rationale']}" for item in payload["objectives"]]
    )
    lines.extend(["", "## Action Items"])
    lines.extend(
        [
            f"- **{item['title']}** | Owner: {item['owner']} | Due: {item['due_window']}"
            for item in payload["action_items"]
        ]
    )
    lines.extend(["", "## Next Steps"])
    lines.extend([f"- {item}" for item in payload["next_steps"]])
    lines.extend(["", "## Risks"])
    lines.extend([f"- {item}" for item in payload["risks"]])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_package(
    transcript_path: str | Path,
    metadata_path: str | Path,
    output_dir: str | Path,
    mode: str = "sample",
) -> dict[str, Any]:
    transcript = _read_text(transcript_path)
    if not transcript:
        raise ValueError("Transcript input is empty.")

    metadata = _read_json(metadata_path)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if mode == "live":
        payload = _build_live_payload(transcript, metadata)
    else:
        payload = _build_sample_payload(transcript)

    validation = validate_payload(payload)
    if not validation["valid"]:
        raise ValueError(f"Deck content failed validation: {validation['errors']}")

    deck_content_path = output_path / "deck_content.json"
    _write_json(deck_content_path, payload)

    validation_report_path = output_path / "validation_report.json"
    validation = validate_file(deck_content_path, validation_report_path)

    summary_path = output_path / "executive_summary.md"
    _write_markdown_summary(summary_path, payload, metadata, mode)

    deck_path = output_path / "meeting_deck.pptx"
    render_presentation(payload, metadata, deck_path)

    return {
        "mode": mode,
        "transcript_path": str(transcript_path),
        "metadata_path": str(metadata_path),
        "output_dir": str(output_path),
        "validation": validation,
        "artifacts": {
            "deck_content": str(deck_content_path),
            "validation_report": str(validation_report_path),
            "summary_markdown": str(summary_path),
            "presentation": str(deck_path),
        },
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build the sample meeting-to-deck artifact package.")
    parser.add_argument("--transcript", default=str(REPO_ROOT / "inputs" / "meeting_transcript.txt"))
    parser.add_argument("--metadata", default=str(REPO_ROOT / "inputs" / "meeting_metadata.json"))
    parser.add_argument("--output-dir", default=str(REPO_ROOT / "artifacts" / "sample_run"))
    parser.add_argument("--mode", choices=("sample", "live"), default="sample")
    args = parser.parse_args()

    result = build_package(args.transcript, args.metadata, args.output_dir, args.mode)
    print(json.dumps(result, indent=2))
