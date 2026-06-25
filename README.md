
# meta-agent

**An agent that builds agents.** Give it a topic or a decision, and it designs a team of expert AI agents, runs them, and synthesizes a final verdict.

Built from scratch in Python over a series of stages — from a single LLM call to a system that picks and builds the right kind of agent system for any task.

---

## The progression

### `foundations/` — the building blocks
- **`agent.py`** — a single agent. Takes a question, calls the LLM, returns an answer.
- **`tool_agent.py`** — a tool-calling agent. The model decides when to call a calculator function and uses the result.
- **`debate.py`** — a two-agent debate. A supporter and a critic argue a topic, then a rebuttal round sharpens it.

### `stage-1-devils-advocate/` — a 5-agent decision stress-tester
Give it any decision. Four expert lenses attack it from independent angles, then a synthesizer delivers a verdict.

- **Skeptic** — exposes the weakest assumptions
- **Risk Analyst** — surfaces worst-case outcomes
- **Pre-Mortem** — assumes it already failed, works backward to why
- **Second-Order Thinker** — traces the consequences most people miss
- **Synthesizer** — combines all four into one sharp recommendation

### `stage-2-meta-agent/` — an agent that designs its own team
Instead of fixed roles, the meta-agent reads your topic, **invents the expert roles** best suited to stress-test it, runs them as a debate, and a senior judge delivers the verdict.

You don't tell it who the experts are. It decides.

### `stage-3-generalized/` — the generalized meta-agent (v1)
Stage 2 always built a debate. Stage 3 goes further: it reads the task and **picks the right structure** before building anything.

- **Router** — decides the approach: `DEBATE`, `PIPELINE`, or `SINGLE`
- **DEBATE** — for judgment calls: invents 3 expert roles, runs them, synthesizes a verdict
- **PIPELINE** — for multi-step tasks: breaks the task into sequential steps, executes each building on the last
- **SINGLE** — for simple questions: routes to one expert for a direct answer

### `stage-4-harness/` — self-verification
The system that checks its own output before it ships. The Reliability Harness runs **two checks** and combines them into one pass/flag verdict:

- **Trust** — is the output internally consistent and free of contradictions? (TRUSTWORTHY / UNTRUSTWORTHY)
- **Groundedness** — does every claim trace back to the given source, with nothing invented? (GROUNDED / UNGROUNDED)

Wired to the meta-agent, it verifies generated output and flags anything that should be regenerated or escalated to a human.

This is the step most "AI agent" projects skip: knowing when *not* to trust the output.

---

## How it works

task / decision
       │
       ▼
   meta-agent (router) ──reads task──► picks structure
       │
       ├──► DEBATE    → invents 3 experts → debate → verdict
       ├──► PIPELINE  → splits into steps → executes in sequence
       └──► SINGLE    → one expert → direct answer

---

## Run it

```bash
# Install
pip install -r requirements.txt

# Add your Groq API key to a .env file:
#   GROQ_API_KEY=your_key_here
# (free key at https://console.groq.com)

# Run any stage
python foundations/agent.py
python stage-1-devils-advocate/devils_advocate.py
python stage-2-meta-agent/meta_agent.py
python stage-3-generalized/meta_agent_v2.py
python stage-4-harness/reliability_harness.py
```

---

## Stack

- **Python 3**
- **Groq** (Llama 3.3 70B) — fast, free-tier LLM inference
- No framework — built directly to understand the agent patterns from the ground up

---

## Why this exists

Most "AI agent" demos are one prompt in a trench coat. This explores what happens when agents start designing *other* agents — and then decide what kind of system a task even needs.

---

*Built by [Krishan Kumar Verma](https://github.com/KrishanKVerma) — building AI agents that ship.*

