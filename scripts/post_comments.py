#!/usr/bin/env python3
"""Script to post code review comments to a PR."""

import json
import os


def main():
    """Read review results and post comments to PR."""
    results_file = "/tmp/review_results.json"

    if not os.path.exists(results_file):
        print("No review results found")
        return

    with open(results_file, "r") as f:
        results = json.load(f)

    # Get GitHub context
    github_event = os.getenv("GITHUB_EVENT_PATH", "")
    if github_event and os.path.exists(github_event):
        with open(github_event, "r") as f:
            event = json.load(f)
    else:
        event = {}

    pr = event.get("pull_request", {})
    pr_number = pr.get("number")
    repo_owner = event.get("repository", {}).get("owner", {}).get("login")
    repo_name = event.get("repository", {}).get("name")

    if not pr_number or not repo_owner or not repo_name:
        print("Could not get PR information from GitHub context")
        return

    print(f"Posting comments for PR #{pr_number} in {repo_owner}/{repo_name}")

    # Summary of results
    total_files = len(results)
    files_with_issues = sum(
        1
        for r in results.values()
        if not isinstance(r.get("total_issues"), str) and r.get("total_issues", 0) > 0
    )

    print(f"  📊 Reviewed {total_files} files")
    print(f"  ⚠️  {files_with_issues} files with issues")

    # Generate summary
    summary = f"""## 🤖 Agentic Code Review Results

### Summary
- **Files Reviewed**: {total_files}
- **Files with Issues**: {files_with_issues}

### Issues Breakdown
"""

    total_critical = 0
    total_high = 0
    total_medium = 0
    total_low = 0

    for file_path, result in results.items():
        if isinstance(result.get("severity_breakdown"), dict):
            total_critical += result["severity_breakdown"].get("critical", 0)
            total_high += result["severity_breakdown"].get("high", 0)
            total_medium += result["severity_breakdown"].get("medium", 0)
            total_low += result["severity_breakdown"].get("low", 0)

    summary += f"""
- 🔴 **Critical**: {total_critical}
- 🟠 **High**: {total_high}
- 🟡 **Medium**: {total_medium}
- 🟢 **Low**: {total_low}

### Files Reviewed
"""

    for file_path, result in results.items():
        if isinstance(result.get("severity_breakdown"), dict):
            issues = result.get("total_issues", 0)
            summary += f"- `{file_path}`: {issues} issues\n"
        else:
            summary += f"- `{file_path}`: ❌ Error\n"

    summary += """
---
*This review was performed by the Agentic Code Reviewer using multiple specialized AI agents.*
"""

    # Print summary (in real scenario, would post to GitHub)
    print("\n" + summary)
    print("\n✓ Review summary generated successfully")


if __name__ == "__main__":
    main()
