import os
import json
import re
import requests
from dotenv import load_dotenv


# ============================================================
# Load Environment
# ============================================================

load_dotenv()


# ============================================================
# Configuration
# ============================================================

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

OPENROUTER_URL = (
    "https://openrouter.ai/api/v1/chat/completions"
)


OPENROUTER_MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "qwen/qwen3-4b:free"
)


# ============================================================
# Validate API Key
# ============================================================

if not OPENROUTER_API_KEY:

    raise RuntimeError(
        "OPENROUTER_API_KEY is not configured. "
        "Please add it to your .env file."
    )


# ============================================================
# Ask AI
# ============================================================

def ask_ollama(
    prompt,
    system_prompt="",
    temperature=0.2,
    json_mode=False
):

    headers = {

        "Authorization":
            f"Bearer {OPENROUTER_API_KEY}",

        "Content-Type":
            "application/json",

        "HTTP-Referer":
            "http://localhost:8501",

        "X-Title":
            "CareerAgent"

    }


    messages = []


    if system_prompt:

        messages.append({

            "role":
                "system",

            "content":
                system_prompt

        })


    messages.append({

        "role":
            "user",

        "content":
            prompt

    })


    payload = {

        "model":
            OPENROUTER_MODEL,

        "messages":
            messages,

        "temperature":
            temperature

    }


    if json_mode:

        payload["response_format"] = {

            "type":
                "json_object"

        }


    response = requests.post(

        OPENROUTER_URL,

        headers=headers,

        json=payload,

        timeout=120

    )


    response.raise_for_status()


    data = response.json()


    choices = data.get(
        "choices",
        []
    )


    if not choices:

        raise RuntimeError(
            "OpenRouter returned no AI response."
        )


    content = choices[0].get(
        "message",
        {}
    ).get(
        "content",
        ""
    )


    if not content:

        raise RuntimeError(
            "OpenRouter returned an empty AI response."
        )


    return content.strip()


# ============================================================
# Extract JSON
# ============================================================

def extract_json(content):

    if isinstance(
        content,
        dict
    ):

        return content


    if not content:

        return {}


    content = str(
        content
    ).strip()


    # --------------------------------------------------------
    # Direct JSON
    # --------------------------------------------------------

    try:

        return json.loads(
            content
        )

    except Exception:

        pass


    # --------------------------------------------------------
    # Remove Markdown Code Fence
    # --------------------------------------------------------

    cleaned = re.sub(

        r"```(?:json)?",

        "",

        content,

        flags=re.IGNORECASE

    )

    cleaned = cleaned.replace(
        "```",
        ""
    ).strip()


    try:

        return json.loads(
            cleaned
        )

    except Exception:

        pass


    # --------------------------------------------------------
    # Find JSON Object
    # --------------------------------------------------------

    start = cleaned.find(
        "{"
    )

    end = cleaned.rfind(
        "}"
    )


    if start >= 0 and end > start:

        candidate = cleaned[
            start:end + 1
        ]


        try:

            return json.loads(
                candidate
            )

        except Exception:

            pass


    return {}