from ai_assistant import ask_qwen

prompt = """
Extract name and current company.

CV:

Ahmed Ashraf EL Sayed Abdelbary

Assistant Manager – Demand & Supply Planning MENA

Samsung Electronics
"""

answer = ask_qwen(prompt)

print(answer)