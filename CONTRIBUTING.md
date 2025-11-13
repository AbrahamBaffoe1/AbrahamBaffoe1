# Contributing Guide

Thank you for your interest in contributing to the Agentic Code Reviewer! This document provides guidelines and instructions.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/agentic-code-reviewer.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Set up development environment (see [SETUP.md](SETUP.md))
5. Make your changes
6. Test thoroughly
7. Submit a pull request

## Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Install code quality tools
pip install black ruff mypy pytest pytest-cov
```

## Code Style

We follow PEP 8 and use `black` for formatting.

```bash
# Format code
black src/ examples/ tests/

# Check code quality
ruff check src/
mypy src/
```

## Testing

All code must be tested. Write tests for new features.

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_language_detector.py -v
```

### Writing Tests

- Place tests in `tests/` directory
- Use descriptive test names: `test_<function>_<scenario>`
- Test both happy path and edge cases
- Example:

```python
def test_language_detection_python():
    """Test Python code detection."""
    code = 'import sys\ndef hello(): pass'
    assert LanguageDetector.detect_by_content(code) == "python"

def test_language_detection_unknown():
    """Test unknown language handling."""
    code = "???"
    assert LanguageDetector.detect_by_content(code) == "unknown"
```

## Documentation

- Update README.md for user-facing changes
- Update SETUP.md for setup changes
- Add docstrings to all functions
- Use type hints for all parameters

### Docstring Example

```python
def analyze_code(self, code: str, file_path: str) -> AgentReview:
    """
    Analyze code and return findings.

    Args:
        code: The source code to analyze
        file_path: Path to the file being analyzed

    Returns:
        AgentReview with findings and analysis

    Raises:
        ValueError: If code is empty
        APIError: If API call fails
    """
```

## Pull Request Process

1. **Update documentation**: Update README or SETUP if needed
2. **Add tests**: Include tests for new features
3. **Run quality checks**:
   ```bash
   black src/ tests/
   ruff check src/ tests/
   mypy src/
   pytest
   ```
4. **Write clear PR description**: Include:
   - What problem does this solve?
   - How does it work?
   - Any breaking changes?
   - Related issues
5. **Keep commits clean**: Squash if needed
6. **Respond to review feedback**: Be open to suggestions

## Adding New Features

### New Agent Type

To add a new review agent (e.g., Performance):

1. Create file: `src/agents/new_agent.py`
2. Extend `ReviewAgent`
3. Implement `get_system_prompt(language)`
4. Register in `src/analyzer.py`
5. Add tests in `tests/test_agents.py`
6. Update README

Example:

```python
from ..core.agent import ReviewAgent

class NewAgent(ReviewAgent):
    """Reviews code for new category."""

    def get_system_prompt(self, language: str = "python") -> str:
        base = "You are an expert in..."
        language_specific = {
            "python": "Additional Python focus...",
            "javascript": "Additional JS focus...",
        }
        return base + language_specific.get(language, "")
```

### Supporting New Language

1. Update `LanguageDetector.detect_by_content()` in `src/language_detector.py`
2. Add language info to `LANGUAGE_EXTENSIONS` and `get_language_info()`
3. Update all agent prompts with language-specific guidance
4. Add examples in `examples/async_example.py`
5. Update README's supported languages list

## Bug Reports

**Found a bug?** Please report it with:

1. **Title**: Clear, specific description
2. **Description**: What happened, what should happen
3. **Steps to reproduce**: Exact steps to trigger the bug
4. **Environment**: Python version, OS, dependencies
5. **Expected vs Actual**: What you expected vs what happened

Example:

```markdown
## Title
Security Agent not detecting SQL injection in parameterized queries

## Description
The security agent is flagging valid parameterized queries as SQL injection vulnerabilities.

## Steps to Reproduce
1. Use code: `cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))`
2. Run: `analyzer.analyze_file("test.py")`
3. Check security findings

## Environment
- Python 3.11
- anthropic==0.32.0

## Expected vs Actual
- **Expected**: No SQL injection finding (safe code)
- **Actual**: Flagged as critical security issue
```

## Feature Requests

Have an idea? Share it!

1. **Title**: Clear feature description
2. **Problem**: What problem does it solve?
3. **Solution**: How should it work?
4. **Alternatives**: Other approaches?
5. **Additional context**: Screenshots, examples, etc.

Example:

```markdown
## Title
Add caching for repeated file analyses

## Problem
Same files analyzed multiple times cause redundant API calls

## Solution
Cache analysis results by file hash, with optional 1-hour TTL

## Additional Context
This would speed up CI/CD pipelines by ~70% in typical cases
```

## Performance Guidelines

- Async/await for I/O operations
- Use `asyncio.gather()` for parallel tasks
- Avoid blocking operations in async context
- Cache when possible
- Monitor API usage

## Security Guidelines

- Never commit API keys or secrets
- Validate all user input
- Use HTTPS for external APIs
- Sanitize error messages (no sensitive data)
- Run security linter: `bandit -r src/`

## Questions?

- Check [README.md](README.md) for documentation
- See [SETUP.md](SETUP.md) for setup issues
- Review existing code for patterns
- Open a discussion in GitHub Issues

## Thank You!

Your contributions make this project better. We appreciate your effort!
