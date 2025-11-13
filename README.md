# 🤖 Agentic Code Reviewer

A sophisticated **multi-agent AI system** for comprehensive code review and quality analysis. This project demonstrates advanced agentic AI patterns with specialized agents that collaborate to provide deep insights into code quality.

## How It Works

1. **Agent Registration**: Each specialized agent registers with the orchestrator
2. **Parallel Analysis**: Orchestrator triggers all agents on the target code
3. **Finding Consolidation**: Results are merged, deduplicated, and prioritized by severity
4. **Report Generation**: Comprehensive report with:
   - Issue counts by severity (Critical, High, Medium, Low, Info)
   - Per-agent findings with recommendations
   - Consolidated summary and top actionable recommendations

## Key Features

- ✅ **Specialized Agents**: 4 expert agents (Security, Performance, Style, Architecture)
- ✅ **Multi-Language Support**: Python, JavaScript/TypeScript, Go, Rust
- ✅ **Async Processing**: Parallel agent execution for faster analysis
- ✅ **Web Dashboard**: Beautiful Flask UI with real-time visualization
- ✅ **GitHub Integration**: Automatic PR reviews with webhook support
- ✅ **CI/CD Ready**: GitHub Actions workflow for automated reviews
- ✅ **Language-Specific Analysis**: Tailored prompts for each language
- ✅ **Structured Output**: JSON-friendly data models for integration
- ✅ **Severity Tracking**: Findings ranked by severity and impact
- ✅ **Actionable Recommendations**: Each issue includes specific fixes
- ✅ **Type Hints**: Full Python type annotations for reliability
- ✅ **Extensible**: Easy to add new agents or languages

## Educational Value

This project demonstrates:
- **Agentic AI Patterns**: Multiple agents specializing in different domains
- **Agent Orchestration**: Coordinating independent agents asynchronously
- **API Integration**: Working with Claude API for AI-powered analysis
- **Async/Await**: Parallel processing with asyncio
- **Language Detection**: Identifying programming languages from code
- **Web Framework**: Building Flask applications with real-time updates
- **GitHub Integration**: Webhook handling and GitHub API usage
- **System Design**: Building modular, extensible, production-ready systems
- **Python Best Practices**: Type hints, structured data, clean architecture

## Implemented Features

- [x] **Async agent execution** for true parallelism
- [x] **GitHub PR integration** (auto-review pull requests)
- [x] **Web dashboard** for result visualization
- [x] **Integration with CI/CD** pipelines (GitHub Actions)
- [x] **Multi-language support** (Python, JS, Go, Rust)
- [x] Language-specific agent prompts
- [x] Webhook handling for GitHub events
- [x] Chart.js visualization of findings

## Future Enhancements

- [ ] Custom agent creation via YAML configuration
- [ ] Caching for repeated analyses
- [ ] Results database/history tracking
- [ ] Team/organization settings
- [ ] API rate limiting and quota management
- [ ] Custom rules and linter integration
- [ ] IDE plugins (VSCode, JetBrains)
- [ ] Slack/Discord notifications
- [ ] Performance benchmarking and trend analysis


## Project Files

- `src/` - Main source code
- `tests/` - Unit and integration tests
- `examples/` - Usage examples
- `scripts/` - Utility scripts for automation
- `.github/workflows/` - CI/CD configuration
- `Makefile` - Common development commands
- `pyproject.toml` - Poetry configuration
- `requirements.txt` - Pip dependencies
- `pytest.ini` - Pytest configuration
- `.pre-commit-config.yaml` - Pre-commit hooks

## Testing

Run tests with:
```bash
make test              # Run tests
make test-cov          # With coverage report
make quality           # Code quality checks
make dev               # Full development workflow
```

## Development

```bash
make dev-install       # Install dev dependencies
make format            # Format code with black
make lint              # Check code quality
make type-check        # Type checking with mypy
```


*Demonstrates: agentic AI • async processing • web frameworks • GitHub integration • multi-language analysis*

