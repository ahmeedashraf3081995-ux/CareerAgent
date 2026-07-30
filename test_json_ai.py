from src.services.llm import ask_ollama, extract_json


prompt = """
Return ONLY valid JSON.

Use exactly this structure:

{
    "score": 95,
    "skills": [
        "Demand Planning",
        "SAP"
    ]
}
"""


response = ask_ollama(
    prompt,
    temperature=0,
    json_mode=True
)


print("RAW RESPONSE:")
print(response)

print()
print("PARSED JSON:")

result = extract_json(response)

print(result)
print()
print("Score:", result.get("score"))
print("Skills:", result.get("skills"))