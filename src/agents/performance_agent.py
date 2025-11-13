"""Performance-focused code review agent."""

from ..core.agent import ReviewAgent


class PerformanceAgent(ReviewAgent):
    """Reviews code for performance issues and optimization opportunities."""

    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        super().__init__(name="Performance", model=model)

    def get_system_prompt(self, language: str = "python") -> str:
        base_prompt = """You are an expert performance engineer reviewing code for:
- Algorithmic inefficiencies (O(n²) loops where O(n) would work)
- Memory leaks and unnecessary allocations
- N+1 query problems and inefficient database access
- Blocking operations in async contexts
- Missing caching or memoization opportunities
- Inefficient data structures
- Excessive logging or I/O operations
- Network optimization issues

Identify performance bottlenecks and suggest concrete optimizations."""

        language_specific = {
            "python": """
Additional focus areas for Python:
- List comprehensions vs loops
- Generator expressions for memory efficiency
- Inefficient regex patterns
- Global Interpreter Lock (GIL) considerations
- Pandas/NumPy vectorization opportunities
- Unnecessary module imports
""",
            "javascript": """
Additional focus areas for JavaScript/TypeScript:
- Event loop blocking operations
- Unnecessary re-renders in React/Vue
- Memory leaks from closures
- Inefficient DOM manipulations
- Bundle size optimization
- Async/await chain optimization
""",
            "go": """
Additional focus areas for Go:
- Goroutine leaks
- Channel inefficiencies
- Mutex contention
- String concatenation in loops (use strings.Builder)
- Unnecessary allocations
- Unbounded goroutine spawning
""",
            "rust": """
Additional focus areas for Rust:
- Unnecessary cloning
- Inefficient string operations
- Heap allocations vs stack
- Copy vs Move semantics
- Iterator chain optimization
- Lock contention in concurrent code
""",
        }

        return base_prompt + language_specific.get(language, "")
