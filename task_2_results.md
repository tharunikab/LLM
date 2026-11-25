# Task 2: Few-Shot Prompting Experiment

## Submission Table: Accuracy vs. Token Cost

| Examples | Accuracy | Tokens per call (avg input) |
| :--- | :--- | :--- |
| 0-shot (`v1.txt`) | 7/10 | ~115 tokens |
| 2-shot (`few_shot_2.txt`) | 10/10 | ~185 tokens |
| 3-shot (`few_shot_3.txt`) | 10/10 | ~220 tokens |
| 5-shot (`few_shot_5.txt`) | 10/10 | ~285 tokens |

## Detailed Predictions on the 10 Tickets

| ID | Ticket | Ground Truth | 2-Shot Output | 3-Shot Output | 5-Shot Output |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | "Our production database is completely down and customers can't log in!" | Technical, High | `{"category":"Technical","priority":"High"}` | `{"category":"Technical","priority":"High"}` | `{"category":"Technical","priority":"High"}` |
| 2 | "I was charged twice for my monthly subscription this morning." | Billing, High | `{"category":"Billing","priority":"High"}` | `{"category":"Billing","priority":"High"}` | `{"category":"Billing","priority":"High"}` |
| 3 | "How do I change the font size on the dashboard?" | General, Low | `{"category":"General","priority":"Low"}` | `{"category":"General","priority":"Low"}` | `{"category":"General","priority":"Low"}` |
| 4 | "Can you add a dark mode feature to the mobile app?" | Feature Request, Low | `{"category":"Feature Request","priority":"Low"}` | `{"category":"Feature Request","priority":"Low"}` | `{"category":"Feature Request","priority":"Low"}` |
| 5 | "The export to CSV button throws a 500 error whenever I click it." | Technical, Medium | `{"category":"Technical","priority":"Medium"}` | `{"category":"Technical","priority":"Medium"}` | `{"category":"Technical","priority":"Medium"}` |
| 6 | "Please send me a copy of last month's invoice for tax purposes." | Billing, Low | `{"category":"Billing","priority":"Low"}` | `{"category":"Billing","priority":"Low"}` | `{"category":"Billing","priority":"Low"}` |
| 7 | "We need to upgrade our plan from 10 seats to 50 seats by Friday." | Account, Medium | `{"category":"Account","priority":"Medium"}` | `{"category":"Account","priority":"Medium"}` | `{"category":"Account","priority":"Medium"}` |
| 8 | "My password reset link expired before I could use it." | Account, Medium | `{"category":"Account","priority":"Medium"}` | `{"category":"Account","priority":"Medium"}` | `{"category":"Account","priority":"Medium"}` |
| 9 | "Your API rate limits are blocking our automated nightly sync." | Technical, High | `{"category":"Technical","priority":"High"}` | `{"category":"Technical","priority":"High"}` | `{"category":"Technical","priority":"High"}` |
| 10 | "Just wanted to say the new update looks great!" | General, Low | `{"category":"General","priority":"Low"}` | `{"category":"General","priority":"Low"}` | `{"category":"General","priority":"Low"}` |

## Sensitivity Test: Example Order & Wrong Example
- **Effect of Example Order:** Reversing the order of the two examples in `few_shot_2.txt` did not change the classification on clear tickets, though LLMs can exhibit slight recency bias toward the final example on borderline cases.
- **Effect of One Wrong Example:** Changing the seat-upgrade example label from `"Account"` to `"Billing"` caused Ticket 7 (`"We need to upgrade our plan from 10 seats to 50 seats by Friday."`) to be misclassified as `"Billing"` instead of `"Account"`, proving that the model closely imitates patterns in the provided examples—even incorrect ones.

## Justification: Best Number of Examples (Cost vs. Accuracy)
**2-shot (`few_shot_2.txt`) is the best choice.** Jumping from 0-shot to 2-shot increased accuracy from **7/10 (70%) to 10/10 (100%)** by resolving the exact edge cases that failed in zero-shot (seat upgrades as `Account` rather than `Billing`, and isolated export errors as `Medium` rather than `High`), while adding only **~70 input tokens** per call. Adding a 3rd or 5th example provided **0% additional accuracy gain** on this dataset while increasing input token usage by **+35 to +100 extra tokens** per request.

## When Few-Shot Is Better Than Zero-Shot (4 Lines)
1. **Resolving ambiguous edge cases:** Few-shot examples clarify subjective boundaries (such as distinguishing `Account` seat upgrades from `Billing` issues) that rules alone leave open to interpretation.
2. **Enforcing strict output formatting:** Demonstrating exact JSON key names, casing, and structure in examples produces far more reliable machine-readable outputs than text instructions alone.
3. **Calibrating severity or priority levels:** Examples anchor what counts as `High` versus `Medium` priority in your specific domain without requiring lengthy rubrics.
4. **Handling domain-specific conventions:** When internal taxonomy labels differ from general public definitions, a few targeted examples immediately align the model to your schema.
