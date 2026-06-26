# meta-agent

**An agent that builds agents — and a harness that checks whether it can be trusted.**

This project is a study in *oversight* of agentic systems. One half generates: a meta-agent that reads a task, designs the right team of expert agents, and runs them. The other half verifies: a reliability harness that takes generated output and asks whether it is actually trustworthy. Built from scratch in Python, stage by stage.

---

## What this investigates

As agents get more capable, the hard problem shifts from *capability* to *oversight*. It is now easy to make an LLM generate plausible output, design a multi-agent workflow, or critique a decision. It is much harder to know whether any of that output is correct. This repo builds both sides of that tension — a generator (the meta-agent) and a verifier (the reliability harness) — to study where automated oversight holds and where it quietly fails. The thesis: **generation is easy; governance is hard.**

---

## The progression

### `foundations/` — the building blocks
- **`agent.py`** — a single agent. Takes a question, calls the LLM, returns an answer.
- **`tool_agent.py`** — a tool-calling agent. The model decides when to call a calculator function and uses the result.
- **`debate.py`** — a two-agent debate. A supporter and a critic argue a topic, then a rebuttal round sharpens it.

### `stage-1-devils-advocate/` — a 5-agent decision stress-tester
Four expert lenses attack a decision from independent angles, then a synthesizer delivers a verdict.

- **Skeptic** — exposes the weakest assumptions
- **Risk Analyst** — surfaces worst-case outcomes
- **Pre-Mortem** — assumes it already failed, works backward to why
- **Second-Order Thinker** — traces the consequences most people miss
- **Synthesizer** — combines all four into one sharp recommendation

### `stage-2-meta-agent/` — an agent that designs its own team
Instead of fixed roles, the meta-agent reads your topic, **invents the expert roles** best suited to stress-test it, runs them as a debate, and a senior judge delivers the verdict. You don't pick the experts. It decides.

### `stage-3-generalized/` — the generalized meta-agent (v1)
Reads the task and **picks the right structure** before building anything.

- **Router** — decides the approach: `DEBATE`, `PIPELINE`, or `SINGLE`
- **DEBATE** — invents 3 expert roles, runs them, synthesizes a verdict
- **PIPELINE** — splits a multi-step task into sequential steps, executes each building on the last
- **SINGLE** — routes to one expert for a direct answer

### `stage-4-harness/` — self-verification
The system that checks its own output before it ships. The Reliability Harness runs **three complementary checks** and combines them into one pass/flag verdict:

- **Trust** — is the output internally consistent and free of contradictions? (TRUSTWORTHY / UNTRUSTWORTHY)
- **Groundedness** — does every claim trace back to a given source, with nothing invented? (GROUNDED / UNGROUNDED)
- **Consistency** — ask the same question several times; do the answers agree, or does the model contradict itself? (CONSISTENT / INCONSISTENT)

`eval_harness.py` measures the harness itself against a labeled test set — not just for accuracy, but for *consistency* across repeated runs.

This is the step most "AI agent" projects skip: knowing when *not* to trust the output.

---

## Research

Two write-ups document what building this actually revealed.

**[Does a Meta-Agent Build Reliable Agents?](docs/writeup-1.md)**
Finding: agents generated for the same task overlap heavily. Reliability comes from the *distinctness* of roles, not the *number* of agents. Generation is easy; governance is hard.

**[Can an LLM Verify Another LLM?](docs/writeup-2.md)**
Finding: an LLM-based verifier reliably catches obvious errors but has reproducible blind spots on subtle and unverifiable claims — they pass every run. It checks whether output *looks* right, not whether it *is* right.

---

## How it works

​```
task / decision
...
reliability harness --> trust + groundedness + consistency --> pass / flag
​```
|

v

meta-agent (router) --> picks structure

|

|--> DEBATE    -> invents 3 experts -> debate -> verdict

|--> PIPELINE  -> splits into steps -> executes in sequence

|--> SINGLE    -> one expert -> direct answer

|

v

reliability harness --> trust + groundedness + consistency --> pass / flag

---

## Run it

```bash
pip install -r requirements.txt

# Add your Groq API key to a .env file:
#   GROQ_API_KEY=your_key_here
# (free key at https://console.groq.com)

python foundations/agent.py
python stage-1-devils-advocate/devils_advocate.py
python stage-2-meta-agent/meta_agent.py
python stage-3-generalized/meta_agent_v2.py
python stage-4-harness/reliability_harness.py
python stage-4-harness/eval_harness.py
```

---

## Limitations & future work

This is a v1 study, and its limits are the interesting part:

- **The harness trusts well-formed text.** Fluent, confident output reads as trustworthy even when it is wrong — format is not truth.
- **It can't verify claims against sources it wasn't given.** With no source, an unverifiable claim (e.g. a revenue figure) passes every time. The harness has no way to know what it doesn't know.
- **LLM-based verification inherits the failures it's meant to catch.** The verifier is itself an LLM, so it shares the same blind spots — most visibly on subtle, near-miss errors.

**Next:** wire in source-grounding so the harness can answer *"I can't verify this"* instead of defaulting to *"looks fine."* The goal is a verifier that knows the boundary of its own knowledge — the real prerequisite for trustworthy automated oversight.

---

## Stack

- **Python 3**
- **Groq** (Llama 3.3 70B) — fast, free-tier LLM inference
- No framework — built directly to study the agent patterns from the ground up

---

*Built by [Krishan Kumar Verma](https://github.com/KrishanKVerma) — building AI agents that ship.*
