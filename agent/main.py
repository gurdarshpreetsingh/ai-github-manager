from pathlib import Path
import os
import subprocess
from datetime import datetime

import ollama
from dotenv import load_dotenv
from github import Github, Auth


# --------------------------------------------------
# Configuration
# --------------------------------------------------

MODEL = "qwen2.5-coder:1.5b"
REPOSITORY = "gurdarshpreetsingh/ai-github-manager"


# --------------------------------------------------
# Environment
# --------------------------------------------------

load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")

if not github_token:
    raise RuntimeError("GITHUB_TOKEN is missing from .env")


# --------------------------------------------------
# AI
# --------------------------------------------------

def ask_ai(prompt):
    """Send a prompt to the local Ollama model."""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


def clean_code(code):
    """Remove Markdown code fences from AI output."""

    code = code.strip()

    if code.startswith("```python"):
        code = code[len("```python"):]

    elif code.startswith("```"):
        code = code[len("```"):]

    if code.endswith("```"):
        code = code[:-3]

    return code.strip()


# --------------------------------------------------
# Project generation
# --------------------------------------------------

def generate_project():

    prompt = """
Create a simple Python project called number_analyzer.

Requirements:

1. Read numbers from command-line arguments.
2. Calculate minimum.
3. Calculate maximum.
4. Calculate average.
5. Print the results clearly.

Return ONLY valid Python code.
Do not include explanations.
Do not use Markdown code fences.
"""

    print("🤖 Generating project with local AI...")

    code = ask_ai(prompt)
    code = clean_code(code)

    project_dir = Path("projects/number_analyzer")
    project_dir.mkdir(parents=True, exist_ok=True)

    project_file = project_dir / "main.py"

    project_file.write_text(
        code,
        encoding="utf-8"
    )

    print(f"✅ Project generated: {project_file}")

    return project_file


# --------------------------------------------------
# Testing
# --------------------------------------------------

def test_project(project_file):

    print("🧪 Testing generated project...")

    command = [
        "python",
        str(project_file),
        "10",
        "20",
        "30",
        "40"
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:

        print("✅ Test passed!")
        print(result.stdout)

        return True

    print("❌ Test failed!")
    print(result.stderr)

    return False


# --------------------------------------------------
# Git helpers
# --------------------------------------------------

def run_git(command):

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:

        print("❌ Git command failed:")
        print(result.stderr)

        raise RuntimeError(
            f"Git command failed: {' '.join(command)}"
        )

    if result.stdout:
        print(result.stdout)

    return result.stdout


def create_branch():

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    branch_name = f"ai/project-{timestamp}"

    print(f"🌿 Creating branch: {branch_name}")

    run_git(["git", "checkout", "-b", branch_name])

    return branch_name


# --------------------------------------------------
# Commit and push
# --------------------------------------------------

def commit_and_push(branch_name):

    print("📦 Adding changes...")

    run_git(["git", "add", "."])

    commit_message = (
        "AI: generate number analyzer project"
    )

    print("💾 Creating commit...")

    run_git(
        [
            "git",
            "commit",
            "-m",
            commit_message
        ]
    )

    print("⬆️ Pushing branch...")

    run_git(
        [
            "git",
            "push",
            "-u",
            "origin",
            branch_name
        ]
    )


# --------------------------------------------------
# Pull Request
# --------------------------------------------------

def create_pull_request(branch_name):

    print("🔀 Creating Pull Request...")

    github = Github(
        auth=Auth.Token(github_token)
    )

    repository = github.get_repo(REPOSITORY)

    pull_request = repository.create_pull(
        title="AI: Generate Number Analyzer",
        body="""
## AI Generated Change

This Pull Request was created automatically by the AI GitHub Manager.

### Changes

- Generated a Python number analyzer
- Tested generated code
- Created a dedicated AI branch
- Automated Git commit
- Automated GitHub push

### Validation

The generated project passed the automated test.

Please review the code before merging.
""",
        head=branch_name,
        base="main"
    )

    print("✅ Pull Request created!")

    print("🔗 Pull Request:")
    print(pull_request.html_url)


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("=" * 60)
    print("       AI GITHUB DEVELOPMENT AGENT")
    print("=" * 60)

    project_file = generate_project()

    test_passed = test_project(project_file)

    if not test_passed:

        print()
        print("⚠️ Generated code failed testing.")
        print("🚫 Pull Request will NOT be created.")

        return

    print()

    branch_name = create_branch()

    commit_and_push(branch_name)

    create_pull_request(branch_name)

    print()
    print("🎉 AI DEVELOPMENT TASK COMPLETED")
    print("👤 Waiting for human review.")
    print()


if __name__ == "__main__":
    main()