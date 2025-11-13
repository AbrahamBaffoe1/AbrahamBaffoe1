"""Architecture and design patterns review agent."""

from ..core.agent import ReviewAgent


class ArchitectureAgent(ReviewAgent):
    """Reviews code for architectural patterns and design principles."""

    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        super().__init__(name="Architecture", model=model)

    def get_system_prompt(self, language: str = "python") -> str:
        base_prompt = """You are an expert software architect reviewing code for:
- SOLID principles violations (Single Responsibility, Open/Closed, etc.)
- Design patterns (missing appropriate patterns)
- Coupling and cohesion issues
- Separation of concerns
- Module structure and organization
- Error handling strategy
- Dependency management
- Testability and mocking concerns
- API design and contracts
- Scalability and extensibility issues

Focus on how the code fits into the larger system architecture."""

        language_specific = {
            "python": """
Additional focus areas for Python:
- Package/module organization
- Abstract base classes and protocols
- Dependency injection patterns
- Factory pattern usage
- Configuration management
- Exception hierarchy design
- Test coverage and testability
""",
            "javascript": """
Additional focus areas for JavaScript/TypeScript:
- Component composition (React/Vue)
- State management architecture
- Module federation
- Separation between business logic and UI
- Observable/Promise patterns
- Dependency injection containers
- Testing strategies (unit, integration, E2E)
""",
            "go": """
Additional focus areas for Go:
- Interface design and composition
- Error handling patterns
- Concurrency patterns (goroutines, channels)
- Package structure and dependencies
- Unexported vs exported symbols
- Context usage in APIs
- Middleware and middleware chains
""",
            "rust": """
Additional focus areas for Rust:
- Trait design and composition
- Error handling (Result vs panic)
- Lifetime correctness
- Interior mutability patterns
- Module organization
- Type system leveraging
- Concurrency primitives (Arc, Mutex)
""",
        }

        return base_prompt + language_specific.get(language, "")
