import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask_agent(system_prompt , user_message):
    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )

    return response.choices[0].message.content


topic = "Formula 1 2026 engine regulations are right or wrong for drivers who want to do raw racing."

supporter = ask_agent(
    "You are a debater who argues strongly in FAVOR of the statement. Give 2 sharp points.",
    topic
)

critic = ask_agent(
    "You are a debater who argues strongly AGAINST the statement. Give 2 sharp points.",
    topic
)

rebuttal = ask_agent(
    "You are a critic. Read the argument below and rebut its specific points directly.",
    f"The argument was:\n{supporter}\n\nNow rebut it."
)

print("FOR:\n" , supporter)
print("\nAGAINST:\n", critic)
print("\nREBUTTAL:\n", rebuttal)