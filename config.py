"""Sam.test — configuration and constants."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

PROMPTS_DIR = BASE_DIR / "prompts"
CASE_DIR = BASE_DIR / "case"
DATA_DIR = BASE_DIR / "data"
ENV_FILE = BASE_DIR / ".env"

TOTAL_ROUNDS = 6

DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"

GROUPS = ["group-exp", "group-ctrl", "group-base"]

# Only group-exp displays the reflection section to participants
GROUPS_WITH_REFLECTION = {"group-exp"}
