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


topic = input("What decision/topic do you want debated? ")

roles_raw = ask_agent(
    "You are a meta-agent that designs debate teams. Given a topic, output exactly 3 expert roles that would best stress-test it. Output ONLY the 3 role names, one per line, nothing else.",
    topic
)

roles = roles_raw.strip().split("\n")

print("\n=== META-AGENT DESIGNED THIS TEAM ===")
for r in roles:
    print("-", r)

    
print("Parsed roles:")
for r in roles:
    print("-",r)


print("\n=== DEBATE ===")
all_arguments = ""
for role in roles:
    argument = ask_agent(
        f"You are a {role}. Give you sharpest 2-point perpectives on the topic.",
        topic
    )
    print(f"\n--- {role} ---")
    print(argument)
    all_arguments += f"\n\n{role}:\n{argument}"

verdict = ask_agent(
    "You are a senior judge. Read these expert perpestives on the topic and give one clear final verdict: the key tensions, and your recommendation. Be direct.",
    f"TOPIC: {topic}\n\nEXPERT VIEWS:{all_arguments}"
)

print("\n=== FINAL VERDICT ===")
print(verdict)