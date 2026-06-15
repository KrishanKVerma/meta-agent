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


task = input("What do you need done? ")

structure = ask_agent(
    "You are a meta-agent that decides how to solve a task. Choose the BEST approach from exactly these three options: DEBATE (for decisions/judgement calls with trade-offs), PIPELINE (for multi-tasks done in sequence), SINGLE (for simple factual or single-expert questions). Output ONLY one word: DEBATE, PIPELINE, or SINGLE.",
    task
)

structure = structure.strip().upper()
print("Meta-agent chose structure:", structure)

if structure == "SINGLE":
    answer = ask_agent(
        f"You are an expert. Answer this clearly and concisely.",
        task
    )
    print("\n=== ANSWER ===\n", answer)

elif structure == "DEBATE":
    topic = input("What decision/topic do you want debated? ")

    roles_raw = ask_agent(
        "You are a meta-agent that designs debate teams. Given a topic, output exactly 3 expert roles that would best stress-test it. Output ONLY the 3 role names, one per line, nothing else.",
        topic
    )

    roles = roles_raw.strip().split("\n")

    print("\n=== META-AGENT DESIGNED THIS TEAM ===")
    for r in roles:
        print("-", r)

    print("\n=== DEBATE ===")
    all_arguments = ""
    for role in roles:
        argument = ask_agent(
            f"You are a {role}. Give your sharpest 2-point perspectives on the topic.",
            topic
        )
        print(f"\n--- {role} ---")
        print(argument)
        all_arguments += f"\n\n{role}:\n{argument}"

    verdict = ask_agent(
        "You are a senior judge. Read these expert perspectives on the topic and give one clear final verdict: the key tensions, and your recommendation. Be direct.",
        f"TOPIC: {topic}\n\nEXPERT VIEWS:{all_arguments}"
    )

    print("\n=== FINAL VERDICT ===")
    print(verdict)

elif structure == "PIPELINE":
    steps_raw = ask_agent(
        "You are a meta-agent that breaks a task into clear sequential steps. Output ONLY the steps, one per line, max 4 steps, nothing else.",
        task
    )
    steps = steps_raw.strip().split("\n")

    print("\n=== META-AGENT PLANNED THESE STEPS ===")
    for s in steps:
        print("-",s)

    print("\n=== EXECUTING PIPELINE ===")
    work_so_far = ""
    for step in steps:
        result = ask_agent(
            f"You are completing one step of a larger task. Do ONLY this step well: {step}",
            f"Original task: {task}\n\nWork done so far:\n{work_so_far}\n\nNow do this step: {step}"
        )
        print(f"\n--- {step} ---")
        print(result)
        work_so_far += f"\n\n{step}:\n{result}"          