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
pip install anthropic pydantic python-dotenv
```

### Usage

**Analyze a single file:**
```python
from src.analyzer import CodeReviewAnalyzer

analyzer = CodeReviewAnalyzer()
result = analyzer.analyze_file("path/to/your/code.py")

print(result["consolidated_summary"])
print(result["top_recommendations"])
```

**Analyze a directory:**
```python
results = analyzer.analyze_directory("src/", pattern="**/*.py")
```

**Run the example:**
```bash
python examples/basic_example.py
```

## 📁 Project Structure

```
agentic-code-reviewer/
├── src/
│   ├── core/
│   │   ├── agent.py          # Base ReviewAgent class
│   │   ├── orchestrator.py    # Coordinates agents
│   │   └── models.py          # Data models
│   ├── agents/
│   │   ├── security_agent.py
│   │   ├── performance_agent.py
│   │   ├── style_agent.py
│   │   └── architecture_agent.py
│   └── analyzer.py            # High-level API
├── examples/
│   └── basic_example.py        # Usage example
├── tests/
│   └── ...                     # Unit tests
└── pyproject.toml             # Dependencies
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

- ✅ **Specialized Agents**: Each agent is an expert in its domain
- ✅ **Extensible**: Easy to add new agents (just extend `ReviewAgent`)
- ✅ **Structured Output**: JSON-friendly data models for integration
- ✅ **Severity Tracking**: Findings ranked by severity and agent expertise
- ✅ **Actionable Recommendations**: Each issue includes specific fixes
- ✅ **Type Hints**: Full Python type annotations for reliability

## 🎓 Educational Value

This project demonstrates:
- **Agentic AI Patterns**: Multiple agents specializing in different domains
- **Agent Orchestration**: Coordinating independent agents for a complex task
- **API Integration**: Working with Claude API for AI-powered analysis
- **System Design**: Building modular, extensible systems
- **Python Best Practices**: Type hints, structured data, clean architecture

## 🚀 Next Steps / Improvements

- [ ] Async agent execution for true parallelism
- [ ] GitHub PR integration (auto-review pull requests)
- [ ] Custom agent creation via configuration
- [ ] Web dashboard for result visualization
- [ ] Integration with CI/CD pipelines
- [ ] Caching for repeated analyses
- [ ] Multi-language support

## 📝 License

MIT

## 🤝 Contributing

Contributions welcome! This is a portfolio project, but feel free to fork and extend it.

---

**Built with ❤️ using Anthropic's Claude API**

