"""DeepSeek API client — tag-based reflection/response parser."""

import re

import requests

from config import DEEPSEEK_BASE_URL, DEEPSEEK_MODEL

_REFLECTION_RE = re.compile(r"<reflection>(.*?)</reflection>", re.DOTALL)
_RESPONSE_RE = re.compile(r"<response>(.*?)</response>", re.DOTALL)


def chat_with_sam(
    messages: list[dict],
    api_key: str,
    group: str,
) -> tuple[str | None, str]:
    """Send chat request, extract <reflection> and <response> from the output.

    Returns (reflection, response).  *reflection* is None when the model
    omits the tag (group-base, group-ctrl) or when the tag is empty.
    """
    url = f"{DEEPSEEK_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": messages,
        "stream": False,
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()

    body = resp.json()
    raw = body["choices"][0]["message"]["content"]
    return _extract(raw)


def _extract(raw: str) -> tuple[str | None, str]:
    """Extract <reflection> and <response> via regex.  Tag-order independent."""
    refl_match = _REFLECTION_RE.search(raw)
    resp_match = _RESPONSE_RE.search(raw)

    reflection = refl_match.group(1).strip() if refl_match else None

    if resp_match:
        response = resp_match.group(1).strip()
    else:
        # Fallback: no <response> tag found — treat entire raw as response
        response = raw.strip()

    return reflection, response
