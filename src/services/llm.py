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
# API Keys
# ============================================================

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


# ============================================================
# Models
# ============================================================

OPENROUTER_MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "openrouter/free"
)

# Groq model
GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b"
)

# Gemini model
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)


# ============================================================
# API URLs
# ============================================================

OPENROUTER_URL = (
    "https://openrouter.ai/api/v1/chat/completions"
)

GROQ_URL = (
    "https://api.groq.com/openai/v1/chat/completions"
)

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
)


# ============================================================
# Build Messages
# ============================================================

def build_messages(
    prompt,
    system_prompt=None
):

    messages = []

    if system_prompt:

        messages.append({
            "role": "system",
            "content": system_prompt
        })

    messages.append({
        "role": "user",
        "content": prompt
    })

    return messages


# ============================================================
# OpenRouter
# ============================================================

def call_openrouter(
    prompt,
    system_prompt=None,
    temperature=0.1,
    json_mode=False,
    timeout=120
):

    if not OPENROUTER_API_KEY:

        raise RuntimeError(
            "OPENROUTER_API_KEY not configured."
        )


    payload = {

        "model":
            OPENROUTER_MODEL,

        "messages":
            build_messages(
                prompt,
                system_prompt
            ),

        "temperature":
            temperature

    }


    if json_mode:

        payload["response_format"] = {
            "type": "json_object"
        }


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


    response = requests.post(

        OPENROUTER_URL,

        headers=headers,

        json=payload,

        timeout=timeout

    )


    if not response.ok:

        raise RuntimeError(
            f"OpenRouter {response.status_code}: "
            f"{response.text[:500]}"
        )


    data = response.json()


    return data[
        "choices"
    ][
        0
    ][
        "message"
    ][
        "content"
    ]


# ============================================================
# Groq
# ============================================================

def call_groq(
    prompt,
    system_prompt=None,
    temperature=0.1,
    json_mode=False,
    timeout=120
):

    if not GROQ_API_KEY:

        raise RuntimeError(
            "GROQ_API_KEY not configured."
        )


    payload = {

        "model":
            GROQ_MODEL,

        "messages":
            build_messages(
                prompt,
                system_prompt
            ),

        "temperature":
            temperature

    }


    if json_mode:

        payload["response_format"] = {
            "type": "json_object"
        }


    headers = {

        "Authorization":
            f"Bearer {GROQ_API_KEY}",

        "Content-Type":
            "application/json"

    }


    response = requests.post(

        GROQ_URL,

        headers=headers,

        json=payload,

        timeout=timeout

    )


    if not response.ok:

        raise RuntimeError(
            f"Groq {response.status_code}: "
            f"{response.text[:500]}"
        )


    data = response.json()


    return data[
        "choices"
    ][
        0
    ][
        "message"
    ][
        "content"
    ]


# ============================================================
# Gemini
# ============================================================

def call_gemini(
    prompt,
    system_prompt=None,
    temperature=0.1,
    json_mode=False,
    timeout=120
):

    if not GEMINI_API_KEY:

        raise RuntimeError(
            "GEMINI_API_KEY not configured."
        )


    url = (
        GEMINI_URL
        +
        GEMINI_MODEL
        +
        ":generateContent"
    )


    contents = []


    if system_prompt:

        contents.append({

            "role":
                "user",

            "parts": [{

                "text":
                    system_prompt

            }]

        })


    contents.append({

        "role":
            "user",

        "parts": [{

            "text":
                prompt

        }]

    })


    payload = {

        "contents":
            contents,

        "generationConfig": {

            "temperature":
                temperature

        }

    }


    if json_mode:

        payload[
            "generationConfig"
        ][
            "responseMimeType"
        ] = "application/json"


    headers = {

        "Content-Type":
            "application/json"

    }


    response = requests.post(

        url,

        params={
            "key":
                GEMINI_API_KEY
        },

        headers=headers,

        json=payload,

        timeout=timeout

    )


    if not response.ok:

        raise RuntimeError(
            f"Gemini {response.status_code}: "
            f"{response.text[:500]}"
        )


    data = response.json()


    return data[
        "candidates"
    ][
        0
    ][
        "content"
    ][
        "parts"
    ][
        0
    ][
        "text"
    ]


# ============================================================
# AI Router
# ============================================================

def ask_ollama(
    prompt,
    system_prompt=None,
    temperature=0.1,
    json_mode=False,
    timeout=120
):

    providers = [

        (
            "OpenRouter",
            call_openrouter
        ),

        (
            "Groq",
            call_groq
        ),

        (
            "Gemini",
            call_gemini
        )

    ]


    errors = []


    for provider_name, provider_function in providers:

        try:

            print(
                f"AI provider: {provider_name}"
            )


            result = provider_function(

                prompt,

                system_prompt=system_prompt,

                temperature=temperature,

                json_mode=json_mode,

                timeout=timeout

            )


            if result:

                print(
                    f"AI success: {provider_name}"
                )

                return result


        except Exception as e:

            error_message = str(e)

            print(
                f"{provider_name} failed:"
            )

            print(
                error_message[:500]
            )


            errors.append({

                "provider":
                    provider_name,

                "error":
                    error_message

            })


            print(
                "Trying next provider..."
            )


    raise RuntimeError(

        "All AI providers failed.\n"
        +
        json.dumps(
            errors,
            indent=2
        )

    )


# ============================================================
# JSON Extraction
# ============================================================

def extract_json(response):

    if not response:

        return {}


    if isinstance(
        response,
        dict
    ):

        return response


    text = str(
        response
    ).strip()


    # Remove markdown fences

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


    # Direct JSON

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


    # Find JSON object

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


    raise ValueError(
        "Could not extract valid JSON "
        "from AI response."
    )