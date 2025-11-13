# Setup Guide

## Prerequisites

- Python 3.11 or higher
- Anthropic API key ([get one here](https://console.anthropic.com/))
- Git (for cloning and development)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd agentic-code-reviewer
```

### 2. Create Virtual Environment (Recommended)

```bash
# Using venv
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n agentic-reviewer python=3.11
conda activate agentic-reviewer
```

### 3. Install Dependencies

**Option A: Using pip (fastest)**
```bash
pip install -r requirements.txt
```

**Option B: Using Poetry**
```bash
pip install poetry
poetry install
# With extras (Flask, requests for web features)
poetry install -E web
```

**Option C: Minimal Installation (core only)**
```bash
pip install anthropic pydantic python-dotenv
```

### 4. Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
ANTHROPIC_API_KEY=your-key-here
```

**Important**: Never commit `.env` to version control!

## Running the Project

### Basic Code Review

```python
from src.analyzer import CodeReviewAnalyzer

analyzer = CodeReviewAnalyzer()
result = analyzer.analyze_file("path/to/code.py")
print(result["consolidated_summary"])
```

### Run Examples

```bash
# Basic example
python examples/basic_example.py

# Async example with multiple languages
python examples/async_example.py
```

### Launch Web Dashboard

```bash
python app.py
# Visit http://localhost:5000
```

### GitHub Integration Setup

1. Create a GitHub personal access token:
   - Go to Settings → Developer settings → Personal access tokens
   - Select "repo" and "read:org" scopes
   - Copy the token

2. Deploy the webhook handler:
   ```python
   from src.github_integration import create_webhook_handler

   app = create_webhook_handler(
       github_token="your_token",
       webhook_secret="your_secret"
   )
   app.run(port=5000)
   ```

3. In your GitHub repo settings:
   - Go to Settings → Webhooks → Add webhook
   - Payload URL: `https://your-server.com/webhook`
   - Content type: `application/json`
   - Events: Pull requests
   - Secret: (use same secret as above)

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_language_detector.py

# Run tests matching a pattern
pytest -k "test_detect"
```

## Development

### Code Style

The project uses `black` for formatting and `ruff` for linting.

```bash
# Format code
black src/ examples/ tests/

# Run linter
ruff check src/

# Type checking
mypy src/
```

### Project Structure

```
├── src/
│   ├── core/              # Core framework
│   ├── agents/            # Specialized review agents
│   ├── analyzer.py        # High-level API
│   ├── language_detector.py
│   ├── github_integration.py
│   └── web_dashboard.py
├── examples/              # Usage examples
├── tests/                 # Unit tests
├── scripts/               # Utility scripts
├── .github/workflows/     # GitHub Actions
├── pyproject.toml         # Poetry config
├── requirements.txt       # pip dependencies
└── README.md              # Project documentation
```

## Troubleshooting

### ImportError: No module named 'anthropic'

**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### ANTHROPIC_API_KEY not found

**Solution**: Create and configure `.env` file
```bash
cp .env.example .env
# Edit .env and add your key
```

### Flask not found (for web dashboard)

**Solution**: Install web dependencies
```bash
pip install flask requests
```

### Tests failing

**Solution**: Ensure pytest is installed
```bash
pip install pytest
pytest tests/
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Your Anthropic API key |
| `FLASK_ENV` | No | Set to `development` for debug mode |
| `GITHUB_TOKEN` | For GitHub integration | GitHub personal access token |

## Advanced Configuration

### Custom Model

To use a different Claude model, modify the agent initialization:

```python
from src.agents import SecurityAgent

agent = SecurityAgent(model="claude-3-opus-20240229")
```

### Async Processing

For faster analysis of multiple files:

```python
import asyncio

async def analyze_multiple():
    analyzer = CodeReviewAnalyzer()
    results = await analyzer.analyze_directory_async("src/")
    return results

asyncio.run(analyze_multiple())
```

### Language-Specific Analysis

The system automatically detects language, but you can verify:

```python
from src.language_detector import LanguageDetector

lang = LanguageDetector.detect_by_content(code, "file.go")
print(f"Detected language: {lang}")
```

## Support

For issues or questions:
1. Check this setup guide
2. See README.md for feature documentation
3. Review example files for usage patterns
4. Check GitHub issues

## Next Steps

- Read [README.md](README.md) for features overview
- Try [examples/basic_example.py](examples/basic_example.py) for basic usage
- Try [examples/async_example.py](examples/async_example.py) for advanced features
- Deploy with GitHub Actions (see `.github/workflows/`)
- Customize agents for your needs
