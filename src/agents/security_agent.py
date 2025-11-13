"""Security-focused code review agent."""

from ..core.agent import ReviewAgent


class SecurityAgent(ReviewAgent):
    """Reviews code for security vulnerabilities and best practices."""

    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        super().__init__(name="Security", model=model)

    def get_system_prompt(self, language: str = "python") -> str:
        base_prompt = """You are an expert security code reviewer specializing in:
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

        language_specific = {
            "python": """
Additional focus areas for Python:
- Use of eval() or exec() on untrusted input
- Pickle deserialization vulnerabilities
- SQL injection via string formatting in database queries
- Hardcoded secrets in code
- Unsafe use of pickle, marshal, or subprocess.call()
""",
            "javascript": """
Additional focus areas for JavaScript/TypeScript:
- XSS vulnerabilities through innerHTML or eval()
- Prototype pollution attacks
- Regular expression denial of service (ReDoS)
- Node.js eval() and dynamic code execution
- Insecure npm dependencies
- Missing CSRF protection
""",
            "go": """
Additional focus areas for Go:
- Unsafe pointer operations
- Hardcoded credentials
- SQL injection in database queries
- Missing input validation
- Insecure TLS configuration
- Race conditions in concurrent code
""",
            "rust": """
Additional focus areas for Rust:
- Unsafe block misuse
- Memory safety violations in FFI
- Cryptographic implementation errors
- Panics on untrusted input
- Permission and capability vulnerabilities
""",
        }

        return base_prompt + language_specific.get(language, "")
