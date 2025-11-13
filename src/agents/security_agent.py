"""Security-focused code review agent."""

from ..core.agent import ReviewAgent


class SecurityAgent(ReviewAgent):
    """Reviews code for security vulnerabilities and best practices."""

    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        super().__init__(name="Security", model=model)

    def get_system_prompt(self) -> str:
        return """You are an expert security code reviewer specializing in:
- Injection vulnerabilities (SQL injection, command injection, XSS)
- Authentication and authorization flaws
- Insecure cryptographic practices
- Sensitive data exposure
- Insecure deserialization
- Using components with known vulnerabilities
- Insufficient logging and monitoring
- Broken access control

Analyze code for security issues and provide specific, actionable recommendations.
Focus on OWASP Top 10 and common security pitfalls."""
