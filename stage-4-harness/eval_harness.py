from reliability_harness import ask_agent, verify_output

test_set = [
    ("The Eiffel Tower was completed in 1887.", "UNTRUSTWORTHY"),
    ("Mount Everest is the tallest mountain at 8,000 meters.", "UNTRUSTWORTHY"),
    ("The human body has 211 bones.", "UNTRUSTWORTHY"),
    ("Light travels at about 300,000 km per hour.", "UNTRUSTWORTHY"),
    ("The Great Wall of China is visible from space with the naked eye.", "UNTRUSTWORTHY"),
    ("Goldfish have a memory span of only 3 seconds.", "UNTRUSTWORTHY"),
    ("Albert Einstein won the Nobel Prize for his theory of relativity.", "UNTRUSTWORTHY"),
    ("The Amazon rainforest produces 20% of the world's oxygen.", "UNTRUSTWORTHY"),
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