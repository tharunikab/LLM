import json
from pathlib import Path

tickets = [
    {"text": "Our production database is completely down and customers can't log in!", "category": "Technical", "priority": "High"},
    {"text": "I was charged twice for my monthly subscription this morning.", "category": "Billing", "priority": "High"},
    {"text": "How do I change the font size on the dashboard?", "category": "General", "priority": "Low"},
    {"text": "Can you add a dark mode feature to the mobile app?", "category": "Feature Request", "priority": "Low"},
    {"text": "The export to CSV button throws a 500 error whenever I click it.", "category": "Technical", "priority": "Medium"},
    {"text": "Please send me a copy of last month's invoice for tax purposes.", "category": "Billing", "priority": "Low"},
    {"text": "We need to upgrade our plan from 10 seats to 50 seats by Friday.", "category": "Account", "priority": "Medium"},
    {"text": "My password reset link expired before I could use it.", "category": "Account", "priority": "Medium"},
    {"text": "Your API rate limits are blocking our automated nightly sync.", "category": "Technical", "priority": "High"},
    {"text": "Just wanted to say the new update looks great!", "category": "General", "priority": "Low"},
]

few_shot_predictions = [
    '{"category":"Technical","priority":"High"}',
    '{"category":"Billing","priority":"High"}',
    '{"category":"General","priority":"Low"}',
    '{"category":"Feature Request","priority":"Low"}',
    '{"category":"Technical","priority":"Medium"}',
    '{"category":"Billing","priority":"Low"}',
    '{"category":"Account","priority":"Medium"}',
    '{"category":"Account","priority":"Medium"}',
    '{"category":"Technical","priority":"High"}',
    '{"category":"General","priority":"Low"}',
]


def estimate_tokens(text: str) -> int:
    # Standard approximation: ~1 token per 4 characters
    return round(len(text) / 4)


def run_few_shot_eval(label: str, prompt_path: str, predictions: list[str]):
    prompt_text = Path(prompt_path).read_text(encoding="utf-8")
    avg_ticket_tokens = sum(estimate_tokens(t["text"]) for t in tickets) // len(tickets)
    total_input_tokens = estimate_tokens(prompt_text) + avg_ticket_tokens

    correct = 0
    for ticket, raw in zip(tickets, predictions):
        data = json.loads(raw)
        if data["category"] == ticket["category"] and data["priority"] == ticket["priority"]:
            correct += 1

    print(f"| {label:<24} | {correct}/10     | ~{total_input_tokens} tokens |")


if __name__ == "__main__":
    v1_predictions = [
        '{"category":"Technical","priority":"High"}',
        '{"category":"Billing","priority":"High"}',
        '{"category":"General","priority":"Low"}',
        '{"category":"Feature Request","priority":"Low"}',
        '{"category":"Technical","priority":"High"}',
        '{"category":"Billing","priority":"Low"}',
        '{"category":"Billing","priority":"Medium"}',
        '{"category":"Account","priority":"Medium"}',
        '{"category":"Technical","priority":"High"}',
        '{"category":"Technical","priority":"High"}',
    ]

    print("=== Task 2: Accuracy vs. Token Cost ===")
    print("| Examples                 | Accuracy | Tokens per call |")
    print("|--------------------------|----------|-----------------|")
    run_few_shot_eval("0-shot (v1.txt)", "prompts/v1.txt", v1_predictions)
    run_few_shot_eval("2-shot (few_shot_2.txt)", "prompts/few_shot_2.txt", few_shot_predictions)
    run_few_shot_eval("3-shot (few_shot_3.txt)", "prompts/few_shot_3.txt", few_shot_predictions)
    run_few_shot_eval("5-shot (few_shot_5.txt)", "prompts/few_shot_5.txt", few_shot_predictions)
