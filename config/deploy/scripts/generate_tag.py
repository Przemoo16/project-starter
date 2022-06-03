import os
import subprocess  # nosec
import sys


def generate_tag() -> str:
    return f"{get_branch_id()}-{get_commit_id()}"


def get_branch_id() -> str:
    with subprocess.Popen(  # nosec
        ["git", "branch"], stdout=subprocess.PIPE
    ) as git_process:
        with subprocess.Popen(  # nosec
            ["grep", "\\*"], stdin=git_process.stdout, stdout=subprocess.PIPE
        ) as grep_process:
            output = subprocess.check_output(  # nosec
                ["cut", "-d", " ", "-f2"], stdin=grep_process.stdout
            )
    current_branch = output.decode("utf-8").strip()
    return os.getenv("CI_BRANCH") or current_branch


def get_commit_id() -> str:
    current_commit = (
        subprocess.check_output(["git", "rev-parse", "HEAD"])  # nosec
        .decode("utf-8")
        .strip()
    )
    return os.getenv("CI_COMMIT_ID") or current_commit


if __name__ == "__main__":
    tag = generate_tag()
    sys.stdout.write(tag)
    sys.stdout.flush()
    sys.exit(0)
