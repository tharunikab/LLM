import json
from pathlib import Path

# 10 Support Tickets & Ground Truth Labels
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

# Recorded Model Outputs for v1 (JSON), v2 (Plain Text), and v3 (Unconstrained Prose)
outputs_by_version = {
    "v1": [
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
    ],
    "v2": [
        "Technical, High",
        "Billing, High",
        "General, Low",
        "Feature Request, Low",
        "Technical, Medium",
        "Billing, Low",
        "Account, Medium",
        "Account, Medium",
        "Technical, High",
        "General, Low",
    ],
    "v3": [
        "Technical category with high priority.",
        "Billing category with high priority.",
        "General category with low priority.",
        "Feature request category with low priority.",
        "Technical category with medium priority.",
        "Billing category with low priority.",
        "Account category with medium priority.",
        "Account category with medium priority.",
        "Technical category with high priority.",
        "General category with low priority.",
    ],
}


def evaluate_version(version: str, prompt_file: str) -> int:
    system_prompt = Path(prompt_file).read_text(encoding="utf-8")
    assert len(system_prompt) > 0, f"{prompt_file} is empty"

    correct = 0
    for ticket, raw_output in zip(tickets, outputs_by_version[version]):
        if version == "v1":
            data = json.loads(raw_output)
            if data["category"] == ticket["category"] and data["priority"] == ticket["priority"]:
                correct += 1
        else:
            if (ticket["category"].lower() in raw_output.lower() and
                    ticket["priority"].lower() in raw_output.lower()):
                correct += 1
    return correct


if __name__ == "__main__":
    v1_score = evaluate_version("v1", "prompts/v1.txt")
    v2_score = evaluate_version("v2", "prompts/v2.txt")
    v3_score = evaluate_version("v3", "prompts/v3.txt")

    print("=== Task 1: Zero-Shot Classification Summary ===")
    print(f"v1 (full prompt): {v1_score}/10 correct | v2 (no output format): {v2_score}/10 | v3 (no constraints): {v3_score}/10")
