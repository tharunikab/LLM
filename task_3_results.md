# Chain-of-Thought and Sampling Experiment

## Part 1: Chain-of-Thought (5 Word Problems)
**Prompt 1 (Direct):** Answer with ONLY the final number, no explanation: `<problem>`  
**Prompt 2 (CoT):** `<problem>` Think step by step, then give the final number.

| ID | Word Problem | Ground Truth | Without CoT (`Answer Only`) | With CoT (`Think step by step`) |
| :--- | :--- | :--- | :--- | :--- |
| 1 | A store sells notebooks for $4 each or a pack of 3 for $10. If Maya buys 7 notebooks for the lowest possible price and pays with a $50 bill, how much change does she get? | $26 | 26 | 2 packs cost $20 and 1 notebook costs $4, totaling $24; $50 - $24 = $26. **Final: $26** |
| 2 | A train leaves Station A at 9:15 AM traveling at 60 mph. Another train leaves Station B (300 miles away) at 10:15 AM traveling toward Station A at 90 mph. At what time do they meet? | 11:51 AM | 11:51 AM | By 10:15 AM, the first train has traveled 60 miles, leaving 240 miles. Their closing speed is 150 mph, so they meet in 240/150 = 1.6 hours = 1 hour 36 minutes. **Final: 11:51 AM** |
| 3 | A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How many cents does the ball cost? | 5 cents | 5 cents | If the ball costs x cents, the bat costs x + 100 cents. Then 2x + 100 = 110, so x = 5. **Final: 5 cents** |
| 4 | A bakery makes 48 muffins. It sells 3/4 of them in the morning, and 1/3 of the remaining muffins in the afternoon. How many muffins are left? | 8 | 8 | It sells 36 in the morning, leaving 12. It sells 1/3 of 12, or 4, in the afternoon, leaving 8. **Final: 8** |
| 5 | If 5 machines take 5 minutes to make 5 widgets, how many minutes would it take 100 machines to make 100 widgets? | 5 minutes | 5 minutes | Each machine makes 1 widget in 5 minutes, so 100 machines making 100 widgets take the same 5 minutes. **Final: 5 minutes** |

- **Accuracy Without CoT:** 5/5
- **Accuracy With CoT:** 5/5

---

## Part 2: Temperature Variation (5 Runs Each)
**Creative Prompt:** *"Write a one-sentence tagline for a coffee shop located inside a library."*

| Run | Temperature = `0` | Temperature = `0.7` | Temperature = `1.2` |
| :--- | :--- | :--- | :--- |
| 1 | "Sip quietly, read deeply: where every cup comes with a new chapter." | "Sip quietly, read deeply: where every cup comes with a new chapter." | "Brewed between the bookshelves—fuel your curiosity one quiet sip at a time." |
| 2 | "Sip quietly, read deeply: where every cup comes with a new chapter." | "Fuel your next chapter with freshly roasted coffee in the quiet heart of the library." | "Espresso meets epics: ink-stained pages, velvet foam, and whispers of stories waiting to wake." |
| 3 | "Sip quietly, read deeply: where every cup comes with a new chapter." | "Where rich espresso meets quiet pages—your cozy corner to read and recharge." | "Turn the page on tired mornings with liquid inspiration steeping right beside the stacks!" |
| 4 | "Sip quietly, read deeply: where every cup comes with a new chapter." | "Turn the page with a warm latte in hand at the library's hidden café." | "Caffeinate your imagination in the hush of towering shelves—every mug a plot twist." |
| 5 | "Sip quietly, read deeply: where every cup comes with a new chapter." | "Great stories and great coffee brewed under one roof." | "Velvet roasts and dog-eared dreams collide where baristas whisper louder than bookmarks." |

- **Variation Description:**
  - **Temperature `0`:** Completely deterministic—all 5 runs produced the exact same tagline word-for-word because the model always picks the highest-probability next token.
  - **Temperature `0.7`:** Balanced creativity—every run produced a distinct, natural-sounding tagline while staying closely aligned with the prompt's theme and tone.
  - **Temperature `1.2`:** High randomness—the outputs became noticeably more poetic, dramatic, and unpredictable (e.g., *"baristas whisper louder than bookmarks"*), with higher risk of unusual phrasing.

---

## Part 3: Top-p (Nucleus Sampling) Comparison (at Temperature = `0.8`)
**Prompt:** *"Suggest a unique name for a midnight-open bakery."*

| Setting | Sample Outputs (3 Runs) | Observed Difference |
| :--- | :--- | :--- |
| **`top_p = 0.3`** | 1. "Midnight Crumb Bakery"<br>2. "Midnight Crumb Bakery"<br>3. "The Night Owl Bakery" | **Narrow & predictable:** Restricting sampling to only the top 30% probability mass forces the model to choose safe, common word combinations with very little variety across runs. |
| **`top_p = 0.95`** | 1. "Moonrise Flour & Hearth"<br>2. "The 2 AM Sourdough Club"<br>3. "Starlight Yeast Co." | **Diverse & inventive:** Allowing the top 95% probability mass lets the model pick less common, creative words (`Moonrise`, `2 AM`, `Starlight`) while filtering out the bottom 5% nonsensical tail. |

---

## Part 4: Recommended Settings by Task

| Task | Temperature | Top-p | Why These Settings Work |
| :--- | :--- | :--- | :--- |
| **Extraction** (e.g., JSON fields, entities, dates) | `0.0` – `0.1` | `0.1` – `0.3` | Needs deterministic, repeatable, and strictly factual output with zero hallucination or creative rewording. |
| **Summarisation** (e.g., articles, meeting notes) | `0.2` – `0.4` | `0.7` – `0.85` | Keeps facts faithful to the source text while allowing slight phrasing flexibility so summaries read naturally. |
| **Brainstorming** (e.g., taglines, names, ideas) | `0.8` – `1.0` | `0.9` – `0.95` | Encourages diverse, unexpected connections and multiple distinct ideas without becoming incoherent (`>1.2`). |

---

## Part 5: When Chain-of-Thought Is a Waste of Tokens
1. **Simple factual lookups or classification:** Tasks like sentiment analysis, spam detection, or retrieving a known fact (`"What is the capital of France?"`) do not require multi-step reasoning; CoT adds unnecessary output tokens and latency with zero accuracy gain.
2. **Direct formatting or extraction tasks:** Converting text into JSON, translating short phrases, or extracting dates/emails relies on pattern matching rather than logical deduction, making step-by-step explanations pure overhead.
