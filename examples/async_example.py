#!/usr/bin/env python3
"""Example using async code review for faster analysis."""

import asyncio
import sys
from pathlib import Path
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analyzer import CodeReviewAnalyzer


async def main():
    """Run async code review example."""
    analyzer = CodeReviewAnalyzer()

    # Example code samples in different languages
    examples = {
        "python_example.py": '''
def fetch_user_data(user_id, db):
    """Fetch user data (vulnerable example)."""
    # SQL injection vulnerability
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    cursor = db.cursor()
    cursor.execute(query)

    # N+1 query problem
    for row in cursor.fetchall():
        posts = db.execute(f"SELECT * FROM posts WHERE user_id = {row[0]}")
        print(posts)
''',
        "javascript_example.js": '''
// XSS vulnerability example
function displayUserComment(comment) {
    const div = document.getElementById('comments');
    div.innerHTML = `<p>${comment}</p>`;  // Vulnerable!
}

// Inefficient event handler
document.addEventListener('mousemove', (event) => {
    // Heavy computation on every mouse move
    document.getElementById('output').innerHTML = performExpensiveCalculation();
});

// Missing error handling
async function fetchData(url) {
    const response = await fetch(url);
    return response.json();
}
''',
        "go_example.go": '''
package main

import "database/sql"

// Race condition example
var counter int

func increment() {
    // Unsafe concurrent access
    counter++
}

// Hardcoded credentials
const dbPassword = "admin123"

func getDB() *sql.DB {
    return sql.Open("postgres", "user=admin password=admin123 dbname=mydb")
}
''',
        "rust_example.rs": '''
// Unsafe code misuse
unsafe fn dangerous_function(ptr: *mut u8) {
    // Dereferencing without validation
    *ptr = 42;
}

// Panic on untrusted input
fn parse_number(input: &str) -> u32 {
    input.parse().unwrap()  // Will panic on invalid input!
}

// Unnecessary clone
fn expensive_operation(data: Vec<u8>) -> Vec<u8> {
    let copy = data.clone();  // Consider moving instead
    expensive_process(copy)
}
''',
    }

    print("🚀 Agentic Code Review - Async Example")
    print("=" * 60)
    print(f"📊 Analyzing {len(examples)} code samples in parallel...\n")

    # Run async analysis for all examples
    start_time = time.time()

    tasks = [
        analyzer.analyze_file_by_content(code, filename)
        for filename, code in examples.items()
    ]

    # Using asyncio.gather to run all analyses concurrently
    # Note: In this case it will appear sequential because analyze_file_by_content
    # uses sync methods. The real async benefit would come from the orchestrator's
    # review_code_async which runs agents in parallel.
    results = await asyncio.gather(
        *[asyncio.to_thread(asyncio.run, _async_wrapper(analyzer, code, filename))
          for filename, code in examples.items()],
        return_exceptions=True
    )

    elapsed = time.time() - start_time

    # Display results
    print(f"\n⏱️  Analysis completed in {elapsed:.2f} seconds\n")

    for (filename, _), result in zip(examples.items(), results):
        if isinstance(result, Exception):
            print(f"\n❌ {filename}: Error - {result}")
            continue

        print(f"\n📄 {filename}")
        print(f"   Total Issues: {result['total_issues']}")
        print(f"   Breakdown: {result['severity_breakdown']['critical']} critical, "
              f"{result['severity_breakdown']['high']} high, "
              f"{result['severity_breakdown']['medium']} medium")

        if result['top_recommendations']:
            print(f"   Top Recommendations:")
            for i, rec in enumerate(result['top_recommendations'][:3], 1):
                print(f"     {i}. {rec[:70]}...")


async def _async_wrapper(analyzer, code, filename):
    """Wrapper to use async with sync function."""
    return await asyncio.to_thread(
        analyzer.analyze_file_by_content, code, filename
    )


if __name__ == "__main__":
    asyncio.run(main())
