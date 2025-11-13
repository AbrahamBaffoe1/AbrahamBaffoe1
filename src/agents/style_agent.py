"""Code style and maintainability review agent."""

from ..core.agent import ReviewAgent


class StyleAgent(ReviewAgent):
    """Reviews code for style, readability, and maintainability."""

    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        super().__init__(name="Style", model=model)

    def get_system_prompt(self) -> str:
        return """You are an expert code style and readability reviewer focusing on:
- Naming conventions (unclear variable/function names)
- Code complexity (functions too long, too many parameters)
- Documentation and comments (missing docstrings)
- Consistent formatting and indentation
- DRY principle violations (repeated code)
- Magic numbers and hardcoded values
- Type hints and annotations
- Readability and cognitive load

Suggest improvements that enhance code maintainability and readability."""
