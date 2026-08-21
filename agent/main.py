from pathlib import Path
import os
import subprocess
from datetime import datetime

import ollama
from dotenv import load_dotenv
from github import Github, Auth


# ============================================================
# CONFIGURATION
# ============================================================

MODEL = "qwen2.5-coder:1.5b"
REPOSITORY = "gurdarshpreetsingh/ai-github-manager"
MAX_ATTEMPTS = 3


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")

if not github_token:
    raise RuntimeError("GITHUB_TOKEN is missing from .env")


# ============================================================
# AI
# ============================================================

def ask_ai(prompt):
    """Ask the local Ollama model for a response."""

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
    """Safely extract Python code from AI output."""

    code = code.strip()

    if "```" in code:

        parts = code.split("```")

        if len(parts) >= 3:

            code = parts[1]

            if code.lstrip().startswith("python"):
                code = code.lstrip()[6:]

    return code.strip()


# ============================================================
# PROJECT GENERATION
# ============================================================

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


# ============================================================
# TESTING
# ============================================================

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

        return True, result.stdout

    print("❌ Test failed!")
    print(result.stderr)

    return False, result.stderr


# ============================================================
# AI SELF-CORRECTION
# ============================================================

def fix_project(project_file, error):

    print("🔧 Asking AI to fix the generated code...")

    current_code = project_file.read_text(
        encoding="utf-8"
    )

    prompt = f"""
You are debugging a Python project.

Current project code:

{current_code}

The program produced this error:

{error}

Fix the Python code so that it works correctly.

Requirements:

1. Return ONLY the complete corrected Python code.
2. Do not use Markdown code fences.
3. Do not explain anything.
4. Preserve the original functionality.
5. Make sure the result is valid Python syntax.
"""

    fixed_code = ask_ai(prompt)

    fixed_code = clean_code(fixed_code)

    project_file.write_text(
        fixed_code,
        encoding="utf-8"
    )

    print("✅ AI generated a corrected version.")


# ============================================================
# GIT
# ============================================================

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

    run_git(
        [
            "git",
            "checkout",
            "-b",
            branch_name
        ]
    )

    return branch_name


def commit_and_push(branch_name):

    print("📦 Adding changes...")

    run_git(
        [
            "git",
            "add",
            "."
        ]
    )

    print("💾 Creating commit...")

    run_git(
        [
            "git",
            "commit",
            "-m",
            "AI: generate number analyzer project"
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


# ============================================================
# PULL REQUEST
# ============================================================

def create_pull_request(branch_name):

    print("🔀 Creating Pull Request...")

    github = Github(
        auth=Auth.Token(github_token)
    )

    repository = github.get_repo(
        REPOSITORY
    )

    pull_request = repository.create_pull(
        title="AI: Generate Number Analyzer",

        body="""
## AI Generated Change

This Pull Request was created automatically
by the AI GitHub Development Agent.

### Changes

- Generated Python project
- Tested generated code
- AI self-correction enabled
- Created dedicated AI branch
- Automated Git commit
- Automated GitHub push

### Validation

The generated project passed automated testing.

Please review the generated code before merging.
""",

        head=branch_name,
        base="main"
    )

    print("✅ Pull Request created!")

    print("🔗 Pull Request:")
    print(pull_request.html_url)


# ============================================================
# MAIN AGENT
# ============================================================

def main():

    print("=" * 60)
    print("       AI GITHUB DEVELOPMENT AGENT")
    print("=" * 60)

    project_file = generate_project()

    for attempt in range(1, MAX_ATTEMPTS + 1):

        print()
        print(
            f"🔄 Test attempt "
            f"{attempt}/{MAX_ATTEMPTS}"
        )

        test_passed, output = test_project(
            project_file
        )

        if test_passed:

            print()
            print("🎉 Code passed testing!")

            branch_name = create_branch()

            commit_and_push(
                branch_name
            )

            create_pull_request(
                branch_name
            )

            print()
            print("🎉 AI DEVELOPMENT TASK COMPLETED")
            print("👤 Waiting for human review.")

            return

        if attempt < MAX_ATTEMPTS:

            print()
            print(
                "🤖 AI will attempt "
                "to fix the error..."
            )

            fix_project(
                project_file,
                output
            )

        else:

            print()
            print(
                "❌ Maximum retry limit reached."
            )

            print(
                "🚫 Pull Request will NOT be created."
            )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()