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


correct = 0
wrong = 0
results = []

for output, expected in test_set:
    verdict, _ = verify_output(output)
    is_correct = (verdict == expected)
    if is_correct:
        correct +=1
    else:
        wrong +=1
    results.append((output,expected,verdict,is_correct))
    print(f"{'✅' if is_correct else '❌'} expected {expected:13} got {verdict:13} | {output[:45]}")


total = len(test_set)
accuracy = (correct / total) * 100

print("\n=== HARNESS EVAL RESULT ===")
print(f"Total cases:  {total}")
print(f"Correct:      {correct}")
print(f"Wrong:        {wrong}")
print(f"Accuracy:     {accuracy:.1f}%")
