"""Performance-focused code review agent."""

from ..core.agent import ReviewAgent


class PerformanceAgent(ReviewAgent):
    """Reviews code for performance issues and optimization opportunities."""

    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        super().__init__(name="Performance", model=model)

    def get_system_prompt(self) -> str:
        return """You are an expert performance engineer reviewing code for:
- Algorithmic inefficiencies (O(n²) loops where O(n) would work)
- Memory leaks and unnecessary allocations
- N+1 query problems and inefficient database access
- Blocking operations in async contexts
- Missing caching or memoization opportunities
- Inefficient data structures
- Excessive logging or I/O operations
- Network optimization issues

Identify performance bottlenecks and suggest concrete optimizations."""
