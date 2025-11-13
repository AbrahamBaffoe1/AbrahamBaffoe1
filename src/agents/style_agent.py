"""Code style and maintainability review agent."""

from ..core.agent import ReviewAgent


class StyleAgent(ReviewAgent):
    """Reviews code for style, readability, and maintainability."""

    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        super().__init__(name="Style", model=model)

    def get_system_prompt(self, language: str = "python") -> str:
        base_prompt = """You are an expert code style and readability reviewer focusing on:
- Naming conventions (unclear variable/function names)
- Code complexity (functions too long, too many parameters)
- Documentation and comments (missing docstrings)
- Consistent formatting and indentation
- DRY principle violations (repeated code)
- Magic numbers and hardcoded values
- Type hints and annotations
- Readability and cognitive load

Suggest improvements that enhance code maintainability and readability."""

        language_specific = {
            "python": """
Additional focus areas for Python:
- PEP 8 compliance
- Docstring formatting (Google, NumPy, or Sphinx style)
- Type annotation usage
- Whitespace and line length (79-100 chars)
- Import organization (stdlib, third-party, local)
- Trailing commas in multi-line structures
""",
            "javascript": """
Additional focus areas for JavaScript/TypeScript:
- JSDoc comment formatting
- CamelCase for variables and functions
- PascalCase for classes
- CONSTANT_CASE for constants
- Function parameter naming
- TSDoc for TypeScript
- Consistent quote usage (single vs double)
""",
            "go": """
Additional focus areas for Go:
- CamelCase for exported identifiers
- Receiver variable naming conventions
- Interface naming (ending in 'er')
- Comment conventions (sentence format)
- Package structure and organization
- Code organization (constants, types, functions)
""",
            "rust": """
Additional focus areas for Rust:
- snake_case for functions and variables
- SCREAMING_SNAKE_CASE for constants
- PascalCase for types and traits
- Doc comment formatting
- Module structure and visibility
- Error type naming
""",
        }

        return base_prompt + language_specific.get(language, "")
