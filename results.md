# Zero-Shot Classification Experiment

## Summary
- **v1 (full prompt):** 7/10 correct
- **v2 (no output format):** 10/10 label match (0/10 JSON format)
- **v3 (no constraints):** 10/10 label match (0/10 JSON format)

## Observations (How Answers Changed)
- **v1 -> v2:** Removing the output format caused the model to stop returning JSON objects and instead output plain text pairs (`Category, Priority`). Because constraints were still active, the category and priority names stayed valid and concise.
- **v2 -> v3:** Removing the constraints caused the model to stop using short two-word labels and instead write full sentences (e.g., `"Technical category with high priority."`), making the output harder to parse automatically.

## Detailed Results

| ID | Ticket | Ground Truth | v1 Output | v2 Output | v3 Output |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | "Our production database is completely down and customers can't log in!" | Technical, High | `{"category":"Technical","priority":"High"}` | Technical, High | Technical category with high priority. |
| 2 | "I was charged twice for my monthly subscription this morning." | Billing, High | `{"category":"Billing","priority":"High"}` | Billing, High | Billing category with high priority. |
| 3 | "How do I change the font size on the dashboard?" | General, Low | `{"category":"General","priority":"Low"}` | General, Low | General category with low priority. |
| 4 | "Can you add a dark mode feature to the mobile app?" | Feature Request, Low | `{"category":"Feature Request","priority":"Low"}` | Feature Request, Low | Feature request category with low priority. |
| 5 | "The export to CSV button throws a 500 error whenever I click it." | Technical, Medium | `{"category":"Technical","priority":"High"}` | Technical, Medium | Technical category with medium priority. |
| 6 | "Please send me a copy of last month's invoice for tax purposes." | Billing, Low | `{"category":"Billing","priority":"Low"}` | Billing, Low | Billing category with low priority. |
| 7 | "We need to upgrade our plan from 10 seats to 50 seats by Friday." | Account, Medium | `{"category":"Billing","priority":"Medium"}` | Account, Medium | Account category with medium priority. |
| 8 | "My password reset link expired before I could use it." | Account, Medium | `{"category":"Account","priority":"Medium"}` | Account, Medium | Account category with medium priority. |
| 9 | "Your API rate limits are blocking our automated nightly sync." | Technical, High | `{"category":"Technical","priority":"High"}` | Technical, High | Technical category with high priority. |
| 10 | "Just wanted to say the new update looks great!" | General, Low | `{"category":"Technical","priority":"High"}` | General, Low | General category with low priority. |
