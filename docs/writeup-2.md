\# Can an LLM Verify Another LLM?



\*A note from building the reliability harness in this repo.\*



\## The question



The harness in `stage-4-harness/` uses an LLM to judge another LLM's output — is it trustworthy, is it grounded, is it consistent? It's an appealing idea: oversight that scales as cheaply as generation. But it has an obvious risk built in — \*\*the verifier is the same kind of system it's supposed to police.\*\*



\## What I found



Measured against a labeled test set of plausible-but-wrong technical claims, the verifier did well on the obvious cases: it reliably flagged clearly false statements (reversed definitions, wrong database categories, inverted facts). Those are \*\*stable-correct\*\* — caught every run.



The failures were the interesting part:



\- \*\*Blind spots are reproducible, not random.\*\* The verifier waved through an unverifiable claim — a revenue figure with no source provided — every single run. It can't flag what it has no way to check, and instead of saying so, it defaults to "looks fine."

\- \*\*Subtle, near-miss errors slip through.\*\* A number that's only slightly off, or a claim that's \*almost\* right, reads as trustworthy to a model judging on plausibility.

\- \*\*Non-determinism on borderline cases (secondary).\*\* On earlier general-knowledge runs, the verifier sometimes gave different verdicts to identical inputs. A domain-specific test set reduced this, but it remains a real failure mode on genuinely ambiguous claims.



\## The takeaway



An LLM verifier \*\*checks whether output looks right, not whether it is right.\*\* It is a plausibility detector wearing the costume of a fact-checker. That makes it useful for catching obvious garbage and useless for catching confident, well-formed errors — which are exactly the errors that matter.



The fix isn't a better prompt. It's \*\*grounding\*\*: giving the verifier real sources to check against, and — just as important — letting it say \*"I can't verify this"\* instead of guessing. A verifier that knows the boundary of its own knowledge is the real prerequisite for trustworthy automated oversight. That's the next stage.

