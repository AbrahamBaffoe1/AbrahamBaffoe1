"""Architecture and design patterns review agent."""

from ..core.agent import ReviewAgent


class ArchitectureAgent(ReviewAgent):
    """Reviews code for architectural patterns and design principles."""

    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        super().__init__(name="Architecture", model=model)

    def get_system_prompt(self) -> str:
        return """You are an expert software architect reviewing code for:
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
