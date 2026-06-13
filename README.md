\# meta-agent



\*\*An agent that builds agents.\*\* Give it a topic or a decision, and it designs a team of expert AI agents, runs them as a multi-perspective debate, and synthesizes a final verdict.



Built from scratch in Python over a series of stages — from a single LLM call to a system that invents its own expert agents on demand.



\---



\## The progression



This repo is built in three stages, each one a step up in capability.



\### `foundations/` — the building blocks

Where it starts: understanding how a single agent works, then how an agent can use tools, then how two agents can argue.



\- \*\*`agent.py`\*\* — a single agent. Takes a question, calls the LLM, returns an answer.

\- \*\*`tool\_agent.py`\*\* — a tool-calling agent. The model decides when to call a calculator function and uses the result.

\- \*\*`debate.py`\*\* — a two-agent debate. A supporter and a critic argue a topic, then a rebuttal round sharpens it.



\### `stage-1-devils-advocate/` — a 5-agent decision stress-tester

Give it any decision. Four expert lenses attack it from independent angles, then a synthesizer delivers a verdict.



\- \*\*Skeptic\*\* — exposes the weakest assumptions

\- \*\*Risk Analyst\*\* — surfaces worst-case outcomes

\- \*\*Pre-Mortem\*\* — assumes it already failed, works backward to why

\- \*\*Second-Order Thinker\*\* — traces the consequences most people miss

\- \*\*Synthesizer\*\* — combines all four into one sharp recommendation



\### `stage-2-meta-agent/` — the flagship: an agent that designs its own team

This is the core idea. Instead of fixed roles, the meta-agent reads your topic, \*\*invents the expert roles\*\* best suited to stress-test it, runs them as a debate, and a senior judge delivers the final verdict.



You don't tell it who the experts are. It decides.



\---



\## How it works



topic / decision



│



▼



meta-agent  ──designs──►  expert roles (invented per topic)



│



▼



debate (each expert argues)



│



▼



synthesizer ──► final verdict





\---



\## Run it



```bash

\# Install

pip install -r requirements.txt



\# Add your Groq API key

\# Create a .env file with:

\#   GROQ\_API\_KEY=your\_key\_here

\# (get a free key at https://console.groq.com)



\# Run any stage

python foundations/agent.py

python stage-1-devils-advocate/devils\_advocate.py

python stage-2-meta-agent/meta\_agent.py

```



\---



\## Stack



\- \*\*Python 3\*\*

\- \*\*Groq\*\* (Llama 3.3 70B) — fast, free-tier LLM inference

\- No framework — built directly to understand the agent patterns from the ground up



\---



\## Why this exists



Most "AI agent" demos are one prompt in a trench coat. This is an exploration of what happens when agents start designing \*other\* agents — the patterns that turn a single LLM call into a system that reasons from multiple perspectives.



\---



\*Built by \[Krishan Kumar Verma](https://github.com/KrishanKVerma) — building AI agents that ship.\*

