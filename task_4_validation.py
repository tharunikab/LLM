import json
from pydantic import BaseModel, ValidationError


# 1. Define the Pydantic Schema
class CandidateProfile(BaseModel):
    name: str
    skills: list[str]
    years_experience: int


# 2. Five Short Resume Paragraphs
resumes = [
    "Ananya Sharma is a backend developer with 4 years of experience building APIs in Python, FastAPI, and PostgreSQL.",
    "Karthik Nair has spent 6 years working as a cloud engineer specializing in AWS, Docker, Kubernetes, and Terraform.",
    "Priya Menon is a frontend engineer with 2 years of experience in React, TypeScript, Tailwind CSS, and Next.js.",
    "Rohan Verma brings 8 years of experience in data engineering using Spark, Kafka, Airflow, and Snowflake.",
    "Divya Krishnan is a fresher with 0 years of professional experience, skilled in Java, Spring Boot, and MySQL.",
]

# 3. Simulated Outputs: Plain Prompting (often wraps in markdown, adds chatter, or uses wrong types)
plain_prompt_outputs = [
    'Here is the extracted JSON:\n```json\n{"name": "Ananya Sharma", "skills": ["Python", "FastAPI", "PostgreSQL"], "years_experience": 4}\n```',  # Invalid raw JSON (markdown + prose)
    '{"name": "Karthik Nair", "skills": ["AWS", "Docker", "Kubernetes", "Terraform"], "years_experience": 6}',  # Valid
    '{"name": "Priya Menon", "skills": "React, TypeScript, Tailwind CSS, Next.js", "years_experience": "two"}',  # Valid JSON syntax, fails Pydantic (skills not list, years not int)
    '{"name": "Rohan Verma", "skills": ["Spark", "Kafka", "Airflow", "Snowflake"], "years_experience": 8}',  # Valid
    '```json\n{"name": "Divya Krishnan", "skills": ["Java", "Spring Boot", "MySQL"], "years_experience": 0}\n```',  # Invalid raw JSON (markdown fences)
]

# 4. Simulated Outputs: JSON Mode (response_format={"type": "json_object"})
json_mode_outputs = [
    '{"name": "Ananya Sharma", "skills": ["Python", "FastAPI", "PostgreSQL"], "years_experience": 4}',
    '{"name": "Karthik Nair", "skills": ["AWS", "Docker", "Kubernetes", "Terraform"], "years_experience": 6}',
    '{"name": "Priya Menon", "skills": ["React", "TypeScript", "Tailwind CSS", "Next.js"], "years_experience": 2}',
    '{"name": "Rohan Verma", "skills": ["Spark", "Kafka", "Airflow", "Snowflake"], "years_experience": 8}',
    '{"name": "Divya Krishnan", "skills": ["Java", "Spring Boot", "MySQL"], "years_experience": 0}',
]


def validate_outputs(label: str, outputs: list[str]) -> int:
    invalid_count = 0
    print(f"\n--- Validating {label} ---")
    for idx, raw in enumerate(outputs, 1):
        try:
            parsed = json.loads(raw)
            profile = CandidateProfile(**parsed)
            print(f"Resume {idx}: VALID -> {profile.model_dump()}")
        except (json.JSONDecodeError, ValidationError) as err:
            invalid_count += 1
            print(f"Resume {idx}: INVALID ({type(err).__name__})")
    return invalid_count


if __name__ == "__main__":
    plain_invalid = validate_outputs("Plain Prompting", plain_prompt_outputs)
    json_mode_invalid = validate_outputs("JSON Mode (response_format)", json_mode_outputs)

    print("\n=== Expected Output Summary ===")
    print(f"Plain prompting: {plain_invalid}/5 invalid JSON | JSON mode: {json_mode_invalid}/5 invalid")
