# Structured Output and Common Mistakes

## Summary
Plain prompting: 3/5 invalid JSON | JSON mode: 0/5 invalid

---

## Part 1: Plain Prompting vs. JSON Mode (`response_format`)

| ID | Resume Paragraph | Plain Prompting Validation (`json.loads` + Pydantic) | JSON Mode Validation (`response_format`) |
| :--- | :--- | :--- | :--- |
| 1 | "Ananya Sharma is a backend developer with 4 years of experience building APIs in Python, FastAPI, and PostgreSQL." | **Invalid** (`JSONDecodeError`: conversational intro + ` ```json ` markdown fences) | **Valid** (`{"name": "Ananya Sharma", "skills": ["Python", "FastAPI", "PostgreSQL"], "years_experience": 4}`) |
| 2 | "Karthik Nair has spent 6 years working as a cloud engineer specializing in AWS, Docker, Kubernetes, and Terraform." | **Valid** | **Valid** |
| 3 | "Priya Menon is a frontend engineer with 2 years of experience in React, TypeScript, Tailwind CSS, and Next.js." | **Invalid** (`ValidationError`: `skills` returned as string instead of `list[str]`, `years_experience` returned as `"two"`) | **Valid** (`{"name": "Priya Menon", "skills": ["React", "TypeScript", "Tailwind CSS", "Next.js"], "years_experience": 2}`) |
| 4 | "Rohan Verma brings 8 years of experience in data engineering using Spark, Kafka, Airflow, and Snowflake." | **Valid** | **Valid** |
| 5 | "Divya Krishnan is a fresher with 0 years of professional experience, skilled in Java, Spring Boot, and MySQL." | **Invalid** (`JSONDecodeError`: wrapped in ` ```json ` code block) | **Valid** (`{"name": "Divya Krishnan", "skills": ["Java", "Spring Boot", "MySQL"], "years_experience": 0}`) |

---

## Part 2: 4 Bad Prompts, Rewrites & Improvement Tests

### 1. Vague Instruction
* **Bad Prompt:** `"Get info from this resume: Ananya Sharma is a backend developer with 4 years of experience in Python and FastAPI."`
* **Bad Output:** `"Ananya Sharma is a backend developer who knows Python and FastAPI and has worked for 4 years."` (Unstructured prose; misses schema keys).
* **Rewritten Prompt:** `"Extract the candidate's full name, technical skills as a list of strings, and total years of experience as an integer from the resume text below."`
* **Improved Output:** `{"name": "Ananya Sharma", "skills": ["Python", "FastAPI"], "years_experience": 4}` (Exact fields and data types extracted).

### 2. No Output Format
* **Bad Prompt:** `"Extract name, skills, and years of experience from: Karthik Nair has 6 years of experience in AWS and Docker."`
* **Bad Output:**
  ```text
  - Name: Karthik Nair
  - Skills: AWS, Docker
  - Years of Experience: 6 years
  ```
  (Fails `json.loads()` completely).
* **Rewritten Prompt:** `"Extract name, skills, and years_experience from the resume. Return ONLY a raw valid JSON object matching {"name": string, "skills": string[], "years_experience": integer} with no markdown fences or extra text."`
* **Improved Output:** `{"name": "Karthik Nair", "skills": ["AWS", "Docker"], "years_experience": 6}` (Passes `json.loads()` and Pydantic directly).

### 3. No Examples (Ambiguous Edge Case / Data Types)
* **Bad Prompt:** `"Return JSON {name, skills[], years_experience} for: Divya Krishnan is a fresher with 0 years of experience, skilled in Java and MySQL."`
* **Bad Output:** `{"name": "Divya Krishnan", "skills": "Java, MySQL", "years_experience": "Fresher (0)"}` (Fails Pydantic validation because `skills` is a string and `years_experience` is not an integer).
* **Rewritten Prompt:**
  ```text
  Return JSON matching {"name": str, "skills": list[str], "years_experience": int}.
  Example Input: "Sam Lee is a junior dev with 0 years experience in Go and Git."
  Example Output: {"name": "Sam Lee", "skills": ["Go", "Git"], "years_experience": 0}
  Now extract from: "Divya Krishnan is a fresher with 0 years of experience, skilled in Java and MySQL."
  ```
* **Improved Output:** `{"name": "Divya Krishnan", "skills": ["Java", "MySQL"], "years_experience": 0}` (100% schema-compliant types).

### 4. Conflicting Instructions
* **Bad Prompt:** `"Return ONLY valid JSON with no extra text. Also write a friendly 2-sentence summary explaining why the candidate is a good fit: Rohan Verma has 8 years in Spark and Kafka."`
* **Bad Output:** `"Rohan Verma is a strong data engineer with 8 years of experience. {"name": "Rohan Verma", "skills": ["Spark", "Kafka"], "years_experience": 8}"` (Contradictory instructions break JSON parsing).
* **Rewritten Prompt:** `"Return ONLY a valid JSON object with keys 'name', 'skills', and 'years_experience'. Do not include any summary, greeting, explanation, or markdown formatting. Text: Rohan Verma has 8 years in Spark and Kafka."`
* **Improved Output:** `{"name": "Rohan Verma", "skills": ["Spark", "Kafka"], "years_experience": 8}` (Clean, single-purpose JSON output with 0 parsing errors).
