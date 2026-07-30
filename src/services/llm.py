import os
import json
import re
import requests
from dotenv import load_dotenv


# ============================================================
# Load Environment
# ============================================================

load_dotenv(
    os.path.join(
        os.path.dirname(__file__),
        ".env"
    )
)


# ============================================================
# OpenRouter Configuration
# ============================================================

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

OPENROUTER_URL = (
    "https://openrouter.ai/api/v1/chat/completions"
)

# ============================================================
# FREE MODEL ROUTER
# ============================================================

OPENROUTER_MODEL = "openrouter/free"


if not OPENROUTER_API_KEY:

    raise RuntimeError(
        "OPENROUTER_API_KEY is not configured. "
        "Please add it to src/services/.env"
    )


# ============================================================
# OpenRouter AI
# ============================================================

def ask_ollama(
    prompt,
    system_prompt=None,
    temperature=0.1,
    json_mode=False,
    timeout=120
):

    messages = []


    # ========================================================
    # System Prompt
    # ========================================================

    if system_prompt:

        messages.append({

            "role":
                "system",

            "content":
                system_prompt

        })


    # ========================================================
    # User Prompt
    # ========================================================

    messages.append({

        "role":
            "user",

        "content":
            prompt

    })


    # ========================================================
    # Request Payload
    # ========================================================

    payload = {

        "model":
            OPENROUTER_MODEL,

        "messages":
            messages,

        "temperature":
            temperature

    }


    # ========================================================
    # JSON Mode
    # ========================================================

    if json_mode:

        payload["response_format"] = {

            "type":
                "json_object"

        }


    # ========================================================
    # Headers
    # ========================================================

    headers = {

        "Authorization":
            f"Bearer {OPENROUTER_API_KEY}",

        "Content-Type":
            "application/json",

        "HTTP-Referer":
            "https://github.com/ahmeedashraf3081995-ux/CareerAgent",

        "X-Title":
            "CareerAgent"

    }


    # ========================================================
    # Send Request
    # ========================================================

    response = requests.post(

        OPENROUTER_URL,

        headers=headers,

        json=payload,

        timeout=timeout

    )


    # ========================================================
    # Error Handling
    # ========================================================

    if not response.ok:

        print(
            "OpenRouter error status:",
            response.status_code
        )

        print(
            "OpenRouter response:",
            response.text
        )


    response.raise_for_status()


    # ========================================================
    # Parse Response
    # ========================================================

    data = response.json()


    # ========================================================
    # Extract AI Response
    # ========================================================

    try:

        content = (
            data[
                "choices"
            ][
                0
            ][
                "message"
            ][
                "content"
            ]
        )

    except (
        KeyError,
        IndexError,
        TypeError
    ):

        raise RuntimeError(

            "OpenRouter returned an unexpected "
            "response: "

            +

            json.dumps(
                data,
                indent=2
            )

        )


    if not content:

        raise RuntimeError(
            "OpenRouter returned an empty response."
        )


    # ========================================================
    # Display Actual Model Used
    # ========================================================

    model_used = data.get(
        "model",
        "unknown"
    )

    print(
        f"OpenRouter free model used: {model_used}"
    )


    return content


# ============================================================
# JSON Extraction
# ============================================================

def extract_json(response):

    if not response:

        return {}


    # ========================================================
    # Already Dictionary
    # ========================================================

    if isinstance(
        response,
        dict
    ):

        return response


    text = str(
        response
    ).strip()


    # ========================================================
    # Remove JSON Markdown Fences
    # ========================================================

    text = re.sub(

        r"^```json\s*",

        "",

        text,

        flags=re.IGNORECASE

    )


    text = re.sub(

        r"^```\s*",

        "",

        text

    )


    text = re.sub(

        r"\s*```$",

        "",

        text

    )


    text = text.strip()


    # ========================================================
    # Direct JSON
    # ========================================================

    try:

        result = json.loads(
            text
        )

        if isinstance(
            result,
            dict
        ):

            return result

    except Exception:

        pass


    # ========================================================
    # Find JSON Object
    # ========================================================

    start = text.find(
        "{"
    )

    end = text.rfind(
        "}"
    )


    if (
        start != -1
        and
        end != -1
        and
        end > start
    ):

        candidate = text[
            start:end + 1
        ]


        try:

            result = json.loads(
                candidate
            )

            if isinstance(
                result,
                dict
            ):

                return result

        except Exception:

            pass


    # ========================================================
    # Unable To Parse
    # ========================================================

    raise ValueError(
        "Could not extract valid JSON from AI response."
    )