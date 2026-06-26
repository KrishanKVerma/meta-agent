\# Does a Meta-Agent Build Reliable Agents?



\*A note from building the meta-agent in this repo.\*



\## The question



A meta-agent designs its own team: given a topic, it invents the expert roles it thinks will best stress-test the problem, then runs them. The appeal is obvious — you don't hand-pick the experts, the system does. But it raises a quieter question: \*\*are the agents it builds actually good?\*\*



\## What I found



Running the meta-agent on real decisions, a pattern showed up fast: the roles it invents often \*\*overlap in reasoning\*\*, even when their titles differ. Asked to stress-test "Should we raise prices by 20%?", it generated a CFO, a Market Research Analyst, and a Consumer Advocate. On paper, three distinct experts. In practice, the CFO and the Market Research Analyst both led with the \*same\* argument — price elasticity reducing sales volume — almost word for word. Only the Consumer Advocate brought a genuinely different lens (affordability and fairness). The debate looked like three perspectives. It was really two.

Adding \*more\* agents did not help. Three overlapping agents produce three overlapping arguments. The quality of the output tracked one thing: \*\*how distinct the roles were from each other.\*\* A skeptic, a pre-mortem analyst, and a second-order thinker disagree productively because they reason differently. Three "experts" who share a worldview just agree louder.



\## The takeaway



Reliability in a multi-agent system comes from \*\*role distinctness, not agent count.\*\* A meta-agent that can generate ten roles is not more useful than one that generates three genuinely different ones — and left unconstrained, it tends to generate similar ones.



This is the first half of a larger lesson this project keeps returning to: \*\*generation is easy, governance is hard.\*\* Getting an agent to produce a team is trivial. Getting it to produce a team that actually covers the problem from independent angles is the real work — and it is a governance problem, not a generation one.

