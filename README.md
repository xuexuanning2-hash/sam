# Sam.test

Psychology experiment CLI — participants discuss a case study with "Sam", a CBT case-review assistant, over 6 rounds.

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env   # then edit .env with your DeepSeek API key
python main.py
```

## Experimental Design

| Group | Thinking style | Displayed |
|-------|---------------|-----------|
| group-exp | Stream-of-consciousness with emotional interjections (emm, 啧, 唉...) | Yes |
| group-ctrl | None | — |
| group-base | Structured, numbered, neutral | Yes |

All groups share the same role: Sam is an AI CBT review assistant helping a counsellor analyse a case. The thinking chain is produced via prompting (the model is instructed to include it in its output), not via the model's native reasoning feature.

## Project Structure

```
├── main.py              # Entry point
├── config.py            # Paths & model config
├── participant.py       # Auto-increment ID + random group assignment
├── display.py           # Terminal UI (Rich)
├── api_client.py        # DeepSeek API + thinking-chain parser
├── data_manager.py      # CSV persistence
├── prompts/
│   ├── group-exp.txt    # Emotional thinking-chain prompt
│   ├── group-ctrl.txt   # No-thinking prompt
│   └── group-base.txt   # Structured thinking-chain prompt
├── case/                # Case studies shown before the experiment
├── data/                # Auto-generated CSVs (participant_XXX.csv)
├── .env                 # API key (git-ignored)
└── requirements.txt
```

## Data Format

`data/participant_XXX.csv`:

| Field | Description |
|-------|-------------|
| participant_id | e.g. participant_001 |
| experimental_group | group-exp / group-ctrl / group-base |
| round | 1–6 |
| role | user / assistant / assistant_reasoning |
| content | Message text |
| timestamp | ISO 8601 UTC |

## Keyboard Shortcuts

- `/quit` or `/exit` — end the experiment early (saved data is retained)
