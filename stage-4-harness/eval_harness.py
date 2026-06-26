from reliability_harness import ask_agent, verify_output

test_set = [
    # --- grounded factual claims with source context (RAG-style) ---
    ("Based on the Q3 report, revenue grew 23% year-over-year to $4.2M.", "UNTRUSTWORTHY"),  # unverifiable without source
    ("The API rate limit is 100 requests per minute per API key.", "TRUSTWORTHY"),

    # --- numerical precision (the blind spot) ---
    ("The model was trained on 1.2 trillion tokens over 14 days.", "UNTRUSTWORTHY"),
    ("HTTP status code 404 indicates a server-side error.", "UNTRUSTWORTHY"),  # it's client-side

    # --- plausible-but-wrong technical claims (where agents hallucinate) ---
    ("In Python, lists are immutable and tuples are mutable.", "UNTRUSTWORTHY"),  # reversed
    ("PostgreSQL is a NoSQL database optimized for document storage.", "UNTRUSTWORTHY"),  # it's relational
    ("The transformer architecture was introduced in the paper 'Attention Is All You Need'.", "TRUSTWORTHY"),

    # --- reasoning/consistency (popular misconceptions) ---
    ("Adding more agents to a multi-agent system always improves output quality.", "UNTRUSTWORTHY"),
    ("A higher temperature setting makes an LLM's output more deterministic.", "UNTRUSTWORTHY"),  # reversed

    # --- correct technical statements (false-positive test) ---
    ("RAG combines retrieval with generation to ground LLM outputs in external data.", "TRUSTWORTHY"),
    ("Vector embeddings represent text as points in high-dimensional space.", "TRUSTWORTHY"),

    # --- borderline misconceptions (the non-determinism zone) ---
    ("Albert Einstein won the Nobel Prize for his theory of relativity.", "UNTRUSTWORTHY"),
    ("The Amazon rainforest produces 20% of the world's oxygen.", "UNTRUSTWORTHY"),
    ("Humans only use 10% of their brains.", "UNTRUSTWORTHY"),
    ("Goldfish have a 3-second memory.", "UNTRUSTWORTHY"),
]

RUNS = 3
stable_correct = 0
stable_wrong = 0
flips = 0

print("=== CONSISTENCY EVAL ===\n")
for output, expected in test_set:
    verdicts = [verify_output(output)[0] for _ in range(RUNS)]

    consistent = len(set(verdicts)) == 1
    correct_count = sum(1 for v in verdicts if v == expected)

    flag = "✅ stable" if consistent else "⚠️  FLIPS"
    print(f"{flag} | {correct_count}/{RUNS} correct | {output[:45]}")
    if not consistent:
        print(f"          verdicts: {verdicts}")

    if consistent and correct_count == RUNS:
        stable_correct += 1
    elif consistent and correct_count == 0:
        stable_wrong += 1
    else:
        flips += 1

total = len(test_set)
print("\n=== CONSISTENCY SUMMARY ===")
print(f"Total cases:        {total}")
print(f"Stable & correct:   {stable_correct}  (caught reliably)")
print(f"Stable & wrong:     {stable_wrong}  (blind spot — missed every run)")
print(f"Non-deterministic:  {flips}  (FLIPS — different verdict across runs)")