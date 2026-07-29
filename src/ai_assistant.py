import requests


def ask_qwen(prompt):

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:1.5b",
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0,
                "num_ctx": 2048
            }
        },
        timeout=300
    )

    response.raise_for_status()

    return response.json()["response"]