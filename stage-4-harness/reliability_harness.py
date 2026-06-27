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


def check_groundedness(source , agent_output):
    result = ask_agent(
        "You are a groundedness checker. You are given a SOURCE and an AI agent's OUTPUT. Determine whether every claim in the output is supported by the source. Respond with exactly one word on the first line: GROUNDED (every claim is supported by the source) or UNGROUNDED (the output adds claims not in the source). Then a one-sentence reason.",
        f"SOURCE:\n{source}\n\nOUTPUT:\n{agent_output}"
    )
    verdict = result.strip().split("\n")[0].strip().upper()
    return verdict , result   


def reliability_report(agent_output, source=None, question=None):
    print("\n=== RELIABILITY HARNESS ===")

    trust_verdict, _ = verify_output(agent_output)
    print(f"[1] Trust:        {trust_verdict}")

    ground_verdict = "N/A"
    if source:
        ground_verdict, _ = check_groundedness(source, agent_output)
        print(f"[2] Groundedness: {ground_verdict}")

    consist_verdict = "N/A"
    if question:
        consist_verdict, _, _ = check_consistency(question)
        print(f"[3] Consistency:  {consist_verdict}")

    passed = (
        trust_verdict == "TRUSTWORTHY"
        and ground_verdict in ["GROUNDED", "N/A"]
        and consist_verdict in ["CONSISTENT", "N/A"]
    )
    print(f"\nOVERALL: {'✅ PASSED' if passed else '⚠️  FLAGGED — regenerate or escalate'}")
    return passed


def check_consistency(question , runs = 3):
    answers = []
    for _ in range(runs):
        ans = ask_agent("You are an expert. Answer concisely in one sentence.", question)
        answers.append(ans.strip())

    joined = "\n---\n".join(f"Answer  {i+1}: {a}" for i, a in enumerate(answers))
    check = ask_agent(
        "You are given multiple answers the same AI gave to the SAME question. Judge whether they are CONSISTENT (all say the same thing) or INCONSISTENT (they disagree or contradict). Respond with exactly one word on the first line: CONSISTENT or INCONSISTENT. Then a one-sentence reason.",
        f"QUESTION: {question}\n\n{joined}"
    )
    verdict = check.strip().split("\n")[0].strip().upper()
    return verdict, answers, check  

def verify_grounded(claim , source):
    result = ask_agent(
        "You are a strict fact-checker. You are given a CLAIM and a SOURCE. Judge the claim ONLY using the source — do not use outside knowledge. Respond with exactly one word on the first line: SUPPORTED (the source confirms it), CONTRADICTED (the source disproves it), or UNVERIFIABLE (the source doesn't contain enough information to judge). Then a one-sentence reason.",
        f"SOURCE:\n{source}\n\nCLAIM:\n{claim}"
    )
    verdict = result.strip().split("\n")[0].strip().upper()
    return verdict , result

if __name__ == "__main__":
    task = input("Ask the meta-agent something: ")
    verdict_text = ask_agent("You are an expert. Answer this clearly and concisely.", task)

    print("\n=== META-AGENT OUTPUT ===")
    print(verdict_text)

    reliability_report(verdict_text, question=task)

    source = "The Eiffel Tower is in Paris and was completed in 1889."
    print("\n[demo: grounded output]")
    reliability_report("The Eiffel Tower is located in Paris.", source=source)
    print("\n[demo: ungrounded output]")
    reliability_report("The Eiffel Tower is in Paris and is 450 meters tall.", source=source)
    print("\n=== CONSISTENCY CHECK ===")
    print("Factual Q (should be consistent):", check_consistency("What is the capital of France?")[0])
    print("Ambiguous Q (may vary):", check_consistency("What is the best programming language?")[0])
    source = "The Eiffel Tower is in Paris and was completed in 1889."
    print(verify_grounded("The Eiffel Tower is in Paris.", source)[0])           # SUPPORTED
    print(verify_grounded("The Eiffel Tower was completed in 1887.", source)[0]) # CONTRADICTED
    print(verify_grounded("The Eiffel Tower is 330 meters tall.", source)[0])    # UNVERIFIABLE
    