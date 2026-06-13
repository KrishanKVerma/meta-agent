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



decision = input("What decision do you want stress-tested? ")

Skeptic = ask_agent(
    "You are a hard skeptic. Attack this decision by exposing its weakest assumptions. Be sharp, 3 points max.",
    decision
)

Risk = ask_agent(
    "You are a risk analyst. Identify the biggest risks and worst-case outcomes of this decision. 3 points max.",
    decision
)

Pre_Mortem = ask_agent(
    "You are a pre-mortem analyst. Assume this decision was made and failed badly. Work backwards and explain the most likely reasons it failed. 3 points max.",
    decision
)

Second_order_Thinker = ask_agent(
    "You are a second-order thinker. Look past the obvious immediate outcome and trace the consequences two to three steps out that most people miss. 3 points max.",
    decision
)

Synthesis = ask_agent(
    "You are a senior advisor. Below are four critical analyses of a decision. Combine them into one sharp verdict: the 3 most serious problems, and your final recommendation. Be direct.",
    f"DECISION: {decision}\n\nSKEPTIC:\n{Skeptic}\n\nRISK:\n{Risk}\n\nPRE-MORTEM:\n{Pre_Mortem}\n\nSECOND-ORDER:\n{Second_order_Thinker}"
)

print("SKEPTIC:\n", Skeptic)
print("\nRISK ANALYST:\n", Risk)
print("\nPre-Mortem:\n" , Pre_Mortem)
print("\nSecond-order Thinker\n", Second_order_Thinker)
print("\n=== FINAL VERDICT ===\n", Synthesis)