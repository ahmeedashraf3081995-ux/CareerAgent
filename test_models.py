import os
import requests
from dotenv import load_dotenv

load_dotenv("src/services/.env")

api_key = os.getenv("OPENROUTER_API_KEY")

response = requests.get(
    "https://openrouter.ai/api/v1/models",
    headers={
        "Authorization": f"Bearer {api_key}"
    }
)

print("STATUS:", response.status_code)

data = response.json()

print("\nFREE MODELS:\n")

for model in data.get("data", []):

    model_id = model.get("id", "")

    if ":free" in model_id:

        pricing = model.get("pricing", {})

        print(
            model_id,
            "| prompt:",
            pricing.get("prompt"),
            "| completion:",
            pricing.get("completion")
        )