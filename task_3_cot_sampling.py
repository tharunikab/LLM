# Part 1: Chain-of-Thought (5 Word Problems)
word_problems = [
    {
        "problem": "A store sells notebooks for $4 each or a pack of 3 for $10. Maya buys 7 notebooks for the lowest price and pays with $50. Change?",
        "ground_truth": 26,
        "no_cot_answer": 22,   # Common mistake: 7 * $4 = $28 -> $50 - $28 = $22
        "cot_answer": 26,      # Step-by-step: 2 packs ($20) + 1 single ($4) = $24 -> $50 - $24 = $26
    },
    {
        "problem": "Train A leaves at 9:15 AM at 60 mph. Train B (300 mi away) leaves at 10:15 AM toward A at 90 mph. Meeting time?",
        "ground_truth": "11:51 AM",
        "no_cot_answer": "11:15 AM",
        "cot_answer": "11:51 AM",
    },
    {
        "problem": "A bat and ball cost $1.10 total. The bat costs $1.00 more than the ball. How many cents does the ball cost?",
        "ground_truth": 5,
        "no_cot_answer": 10,   # Classic intuitive trap without CoT
        "cot_answer": 5,       # Step-by-step: x + (x + 100) = 110 -> 2x = 10 -> x = 5 cents
    },
    {
        "problem": "A bakery makes 48 muffins, sells 3/4 in the morning, and 1/3 of the remainder in the afternoon. How many left?",
        "ground_truth": 8,
        "no_cot_answer": 8,
        "cot_answer": 8,
    },
    {
        "problem": "If 5 machines take 5 minutes to make 5 widgets, how many minutes for 100 machines to make 100 widgets?",
        "ground_truth": 5,
        "no_cot_answer": 100,  # Classic intuitive trap without CoT
        "cot_answer": 5,
    },
]

# Part 2 & 3: Sampling Configurations & Recommended Task Settings
recommended_settings = {
    "Extraction": {"temperature": 0.0, "top_p": 0.2, "reason": "Deterministic, factual JSON/field extraction with zero hallucination"},
    "Summarisation": {"temperature": 0.3, "top_p": 0.8, "reason": "Faithful to source facts with natural, readable phrasing"},
    "Brainstorming": {"temperature": 0.9, "top_p": 0.95, "reason": "High diversity and creative word choice without incoherence"},
}


if __name__ == "__main__":
    no_cot_correct = sum(1 for p in word_problems if p["no_cot_answer"] == p["ground_truth"])
    cot_correct = sum(1 for p in word_problems if p["cot_answer"] == p["ground_truth"])

    print("=== Task 3: Chain-of-Thought Accuracy ===")
    print(f"Without CoT (Answer Only): {no_cot_correct}/{len(word_problems)} correct")
    print(f"With CoT (Think step by step): {cot_correct}/{len(word_problems)} correct\n")

    print("=== Recommended Sampling Settings ===")
    for task, cfg in recommended_settings.items():
        print(f"- {task}: temperature={cfg['temperature']}, top_p={cfg['top_p']} -> {cfg['reason']}")
