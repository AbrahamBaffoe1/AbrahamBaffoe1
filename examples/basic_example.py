#!/usr/bin/env python3
"""Basic example of using the code review analyzer."""

import json
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analyzer import CodeReviewAnalyzer


def main():
    """Run a basic code review example."""
    analyzer = CodeReviewAnalyzer()

    # Example code to review
    example_code = '''
def process_user_input(user_data):
    """Process user input and store in database."""
    import sqlite3

    # Create connection (inefficient - should reuse)
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # Security issue: SQL injection vulnerability
    query = f"INSERT INTO users VALUES ('{user_data}')"
    cursor.execute(query)

    # Performance issue: no indexing
    for i in range(1000000):
        cursor.execute(f"SELECT * FROM users WHERE id = {i}")

    # Style issue: unclear variable naming
    x = len(user_data)
    y = x * 2
    z = y / x if x != 0 else 0

    return z
'''

    # Write example code to temp file
    example_file = Path("/tmp/example_code.py")
    example_file.write_text(example_code)

    print("🔍 Analyzing example code with multi-agent system...")
    print("=" * 60)

    # Run analysis
    result = analyzer.analyze_file(str(example_file))

    # Pretty print results
    print(f"\n📄 File: {result['file_name']}")
    print(f"📊 Total Issues: {result['total_issues']}")
    print(f"\n🎯 Severity Breakdown:")
    for severity, count in result["severity_breakdown"].items():
        print(f"  - {severity.capitalize()}: {count}")

    print(f"\n📝 Consolidated Summary:")
    print(result["consolidated_summary"])

    print(f"\n💡 Top Recommendations:")
    for i, rec in enumerate(result["top_recommendations"], 1):
        print(f"  {i}. {rec}")

    print(f"\n📋 Detailed Agent Reviews:")
    for agent_name, review in result["agent_reviews"].items():
        if review["findings"]:
            print(f"\n  {agent_name} Agent ({len(review['findings'])} findings):")
            print(f"    Summary: {review['summary']}")
            for finding in review["findings"][:3]:  # Show first 3
                print(
                    f"    - [{finding['severity'].upper()}] Line {finding['line_number']}: {finding['description']}"
                )

    print("\n" + "=" * 60)
    print("✅ Analysis complete!")


if __name__ == "__main__":
    main()
