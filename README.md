# 🤖 Agentic Code Reviewer

A sophisticated **multi-agent AI system** for comprehensive code review and quality analysis. This project demonstrates advanced agentic AI patterns with specialized agents that collaborate to provide deep insights into code quality.

## 🎯 What is This?

Instead of a single monolithic code reviewer, this system deploys **4 specialized AI agents**, each an expert in their domain:

- **🔐 Security Agent**: Detects vulnerabilities (SQL injection, XSS, auth flaws, etc.)
- **⚡ Performance Agent**: Identifies bottlenecks (algorithmic issues, memory leaks, N+1 queries)
- **🎨 Style Agent**: Reviews readability, naming, structure, and maintainability
- **🏗️ Architecture Agent**: Analyzes design patterns, SOLID principles, coupling/cohesion

Each agent independently analyzes code, then results are consolidated into a comprehensive report.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Anthropic API key ([get one here](https://console.anthropic.com/))

### Installation

1. Clone and setup:
```bash
git clone <this-repo>
cd agentic-code-reviewer
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

2. Install dependencies:
```bash
# Core dependencies
pip install anthropic pydantic python-dotenv

# For web dashboard and GitHub integration
pip install -e ".[web]"
# or
pip install flask requests
```

### Usage

**Basic Analysis (Synchronous):**
```python
from src.analyzer import CodeReviewAnalyzer

analyzer = CodeReviewAnalyzer()
result = analyzer.analyze_file("path/to/your/code.py")

print(result["consolidated_summary"])
print(result["top_recommendations"])
```

**Async Analysis (Parallel Agent Execution):**
```python
import asyncio
from src.analyzer import CodeReviewAnalyzer

async def main():
    analyzer = CodeReviewAnalyzer()
    result = await analyzer.analyze_file_async("path/to/your/code.py")
    print(result["consolidated_summary"])

asyncio.run(main())
```

**Analyze a directory:**
```python
results = analyzer.analyze_directory("src/", pattern="**/*.py")
```

**Web Dashboard:**
```bash
python app.py
# Visit http://localhost:5000 in your browser
```

**GitHub PR Integration:**
```python
from src.github_integration import create_webhook_handler

app = create_webhook_handler(
    github_token="your_github_token",
    webhook_secret="your_webhook_secret"
)
app.run(port=5000)
```

**Run examples:**
```bash
# Basic synchronous example
python examples/basic_example.py

# Async example with multiple languages
python examples/async_example.py
```

## 📁 Project Structure

```
agentic-code-reviewer/
├── src/
│   ├── core/
│   │   ├── agent.py              # Base ReviewAgent class (sync + async)
│   │   ├── orchestrator.py        # Coordinates agents (sync + async)
│   │   └── models.py              # Data models
│   ├── agents/
│   │   ├── security_agent.py      # Multi-language security review
│   │   ├── performance_agent.py   # Multi-language performance review
│   │   ├── style_agent.py         # Multi-language style review
│   │   └── architecture_agent.py  # Multi-language architecture review
│   ├── analyzer.py                # High-level API (sync + async)
│   ├── language_detector.py       # Language detection
│   ├── github_integration.py      # GitHub webhook + PR reviewer
│   └── web_dashboard.py           # Flask web dashboard
├── .github/workflows/
│   └── code-review.yml            # GitHub Actions CI/CD workflow
├── scripts/
│   ├── review_pr.py               # PR review script
│   └── post_comments.py           # Comment posting script
├── examples/
│   ├── basic_example.py           # Basic usage example
│   └── async_example.py           # Async + multi-language example
├── app.py                         # Flask app entry point
├── pyproject.toml                 # Project dependencies
└── README.md                      # This file
```

## 🔧 How It Works

1. **Agent Registration**: Each specialized agent registers with the orchestrator
2. **Parallel Analysis**: Orchestrator triggers all agents on the target code
3. **Finding Consolidation**: Results are merged, deduplicated, and prioritized by severity
4. **Report Generation**: Comprehensive report with:
   - Issue counts by severity (Critical, High, Medium, Low, Info)
   - Per-agent findings with recommendations
   - Consolidated summary and top actionable recommendations

## 💡 Key Features

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

## 🎓 Educational Value

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

## 🚀 Implemented Features

- [x] **Async agent execution** for true parallelism
- [x] **GitHub PR integration** (auto-review pull requests)
- [x] **Web dashboard** for result visualization
- [x] **Integration with CI/CD** pipelines (GitHub Actions)
- [x] **Multi-language support** (Python, JS, Go, Rust)
- [x] Language-specific agent prompts
- [x] Webhook handling for GitHub events
- [x] Chart.js visualization of findings

## 🔄 Future Enhancements

- [ ] Custom agent creation via YAML configuration
- [ ] Caching for repeated analyses
- [ ] Results database/history tracking
- [ ] Team/organization settings
- [ ] API rate limiting and quota management
- [ ] Custom rules and linter integration
- [ ] IDE plugins (VSCode, JetBrains)
- [ ] Slack/Discord notifications
- [ ] Performance benchmarking and trend analysis

## 📝 License

MIT

## 🤝 Contributing

Contributions welcome! This is a portfolio project, but feel free to fork and extend it.

---

**Built with ❤️ using Anthropic's Claude API**

