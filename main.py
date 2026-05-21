#!/usr/bin/env python3
"""Sam.test — Psychology Experiment CLI.

A local command-line dialogue system where participants interact with
"Sam", a CBT case-review assistant, over 6 rounds.  Participant IDs are
auto-assigned, groups are randomly allocated, and every round is
persisted to CSV inside the data/ folder.
"""

import argparse
import os
import sys

# ── enforce UTF-8 before anything else ───────────────────────────────────
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from datetime import datetime, timezone

from dotenv import load_dotenv

from config import PROMPTS_DIR, CASE_DIR, ENV_FILE, TOTAL_ROUNDS, GROUPS_WITH_REFLECTION
from participant import get_next_participant_id, assign_group
from data_manager import ensure_data_dir, save_round
from display import (
    clear_screen,
    print_header,
    print_case,
    print_round_header,
    print_reflection,
    print_response,
    print_rating_prompt,
    get_user_input,
    get_rating_input,
    print_goodbye,
    console,
)
from api_client import chat_with_sam


def _load_case() -> str:
    """Load and concatenate all files in the case/ folder."""
    parts: list[str] = []
    for cf in sorted(CASE_DIR.iterdir()):
        if cf.is_file():
            parts.append(cf.read_text(encoding="utf-8").strip())
    return "\n\n".join(parts)


def _load_prompt(group: str) -> str:
    path = PROMPTS_DIR / f"{group}.txt"
    if not path.exists():
        console.print(f"[red]Missing prompt file: {path}[/red]")
        sys.exit(1)
    return path.read_text(encoding="utf-8").strip()


def main() -> None:
    # ── CLI flags for testing ────────────────────────────────────────────
    parser = argparse.ArgumentParser(description="Sam.test experiment runner")
    parser.add_argument(
        "--group",
        choices=["group-exp", "group-ctrl", "group-base"],
        default=None,
        help="Force a specific experimental group (skip random assignment).",
    )
    args = parser.parse_args()

    # ── environment ───────────────────────────────────────────────────────
    load_dotenv(ENV_FILE)
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        console.print("[red]Error: DEEPSEEK_API_KEY not found in .env[/red]")
        sys.exit(1)

    ensure_data_dir()

    # ── participant setup ─────────────────────────────────────────────────
    participant_id = get_next_participant_id()
    group = args.group if args.group else assign_group()
    system_prompt = _load_prompt(group)
    show_reflection = group in GROUPS_WITH_REFLECTION

    # ── pre-experiment case display ───────────────────────────────────────
    case_content = _load_case()
    clear_screen()
    print_header()
    if case_content:
        print_case(case_content)
    input("\nPress Enter to begin the conversation...")

    # ── dialogue rounds ───────────────────────────────────────────────────
    messages: list[dict] = [{"role": "system", "content": system_prompt}]

    for rnd in range(1, TOTAL_ROUNDS + 1):
        print_round_header(rnd, TOTAL_ROUNDS)
        user_input = get_user_input()

        if user_input.lower() in {"/quit", "/exit"}:
            console.print("[dim]Experiment ended early by participant.[/dim]")
            break

        messages.append({"role": "user", "content": user_input})
        now = datetime.now(timezone.utc).isoformat()
        save_round(participant_id, group, rnd, "user", user_input, now)

        reflection, response = chat_with_sam(messages, api_key, group)

        messages.append({"role": "assistant", "content": response})
        now = datetime.now(timezone.utc).isoformat()

        if reflection and show_reflection:
            print_reflection(reflection)
            save_round(participant_id, group, rnd, "assistant_reasoning", reflection, now)

        print_response(response)
        save_round(participant_id, group, rnd, "assistant", response, now)

        # ── transparency rating after rounds 3 and 6 ─────────────────────
        if rnd in {3, 6}:
            print_rating_prompt()
            rating = get_rating_input()
            rating_ts = datetime.now(timezone.utc).isoformat()
            save_round(participant_id, group, rnd, "rating", rating, rating_ts)

    # ── done ──────────────────────────────────────────────────────────────
    print_goodbye(participant_id, group)


if __name__ == "__main__":
    main()
