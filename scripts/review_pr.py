#!/usr/bin/env python3
"""Script to review changed files in a PR."""

import json
import os
import subprocess
from pathlib import Path

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analyzer import CodeReviewAnalyzer


def get_changed_files():
    """Get list of changed files in the PR."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "origin/main...HEAD"],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip().split("\n") if result.stdout.strip() else []


def should_review_file(file_path: str) -> bool:
    """Check if file should be reviewed."""
    extensions = {".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs"}
    ext = "." + file_path.split(".")[-1] if "." in file_path else ""
    return ext in extensions


def main():
    """Review changed files and save results."""
    changed_files = get_changed_files()

    print(f"Found {len(changed_files)} changed files")

    # Filter files to review
    files_to_review = [f for f in changed_files if should_review_file(f) and os.path.exists(f)]

    if not files_to_review:
        print("No files to review")
        return

    analyzer = CodeReviewAnalyzer()
    results = {}

    print(f"Reviewing {len(files_to_review)} files...")

    for file_path in files_to_review:
        print(f"  📄 {file_path}...", end=" ", flush=True)
        try:
            result = analyzer.analyze_file(file_path)
            results[file_path] = result
            print(f"✓ ({result['total_issues']} issues)")
        except Exception as e:
            print(f"✗ Error: {e}")
            results[file_path] = {"error": str(e)}

    # Save results to file
    with open("/tmp/review_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to /tmp/review_results.json")


if __name__ == "__main__":
    main()
