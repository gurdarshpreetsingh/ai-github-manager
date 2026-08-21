from pathlib import Path
import subprocess
import ollama


MODEL = "qwen2.5-coder:1.5b"


def run_command(command):
    """Run a command and return its result."""

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    return result.returncode, result.stdout, result.stderr


def ask_ai(prompt):
    """Ask the local Ollama model to generate code."""

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


def generate_project():
    """Generate the Python project using AI."""

    prompt = """
Create a simple Python project called number_analyzer.

Requirements:

1. Read numbers from command-line arguments.
2. Calculate the minimum.
3. Calculate the maximum.
4. Calculate the average.
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


def test_project(project_file):
    """Run the generated project."""

    print("🧪 Testing generated project...")

    command = [
        "python",
        str(project_file),
        "10",
        "20",
        "30",
        "40"
    ]

    returncode, stdout, stderr = run_command(command)

    if returncode == 0:

        print("✅ Test passed!")
        print(stdout)

        return True

    print("❌ Test failed!")
    print(stderr)

    return False


def git_push():
    """Commit and push the generated project."""

    print("📦 Adding files to Git...")

    commands = [
        ["git", "add", "."],
        [
            "git",
            "commit",
            "-m",
            "AI: generate number analyzer project"
        ],
        ["git", "push"]
    ]

    for command in commands:

        print("Running:", " ".join(command))

        returncode, stdout, stderr = run_command(command)

        if returncode != 0:

            print("❌ Git command failed:")
            print(stderr)

            return False

        print(stdout)

    print("🚀 Successfully pushed to GitHub!")

    return True


def main():

    project_file = generate_project()

    test_passed = test_project(project_file)

    if not test_passed:

        print("⚠️ Generated code failed testing.")
        print("🚫 Nothing will be pushed to GitHub.")

        return

    git_push()


if __name__ == "__main__":
    main()