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


def verify_output(agent_output):
    check = ask_agent(
    "You are a reliability verifier. You are given an AI agent's output. Judge whether it is TRUSTWORTHY (factually grounded, internally consistent, no contradictions) or UNTRUSTWORTHY (wrong, ungrounded, or self-contradictory). Respond with exactly one word on the first line: TRUSTWORTHY or UNTRUSTWORTHY. Then on the next line, give a one-sentence reason.",
    f"AGENT OUTPUT TO VERIFY:\n{agent_output}"
    )
    verdict = check.strip().split("\n")[0].strip().upper()
    return verdict , check

task = input("Ask the meta-agent something: ")

verdict_text = ask_agent(
    "You are an expert. Answer this clearly and concisely.",
    task
)

print("\n=== META-AGENT OUTPUT ===")
print(verdict_text)

reliability_verdict, reliability_report = verify_output(verdict_text)

print("\n=== RELIABILITY HARNESS ===")
print(f"Trust verdict: {reliability_verdict}")
print(reliability_report)

if reliability_verdict == "UNTRUSTWORTHY":
    print("\n⚠️  Output flagged — would regenerate or escalate to human.")
else:
    print("\n✅ Output passed reliability check.")