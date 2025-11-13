.PHONY: help install dev-install test test-cov lint format type-check clean run-web run-example run-async

help:
	@echo "Available commands:"
	@echo "  make install       - Install production dependencies"
	@echo "  make dev-install   - Install all dependencies including dev tools"
	@echo "  make test          - Run tests"
	@echo "  make test-cov      - Run tests with coverage report"
	@echo "  make lint          - Check code quality with ruff"
	@echo "  make format        - Format code with black"
	@echo "  make type-check    - Run type checking with mypy"
	@echo "  make quality       - Run all quality checks (lint + type-check)"
	@echo "  make clean         - Clean up cache and build files"
	@echo "  make run-web       - Launch web dashboard"
	@echo "  make run-example   - Run basic example"
	@echo "  make run-async     - Run async example"

install:
	pip install -r requirements.txt

dev-install:
	pip install -r requirements.txt
	pip install pytest pytest-cov black ruff mypy

test:
	pytest tests/

test-cov:
	pytest tests/ --cov=src --cov-report=html --cov-report=term

lint:
	ruff check src/ tests/ examples/

format:
	black src/ tests/ examples/ scripts/

type-check:
	mypy src/

quality: lint type-check

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name *.egg-info -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name .DS_Store -delete

run-web:
	python app.py

run-example:
	python examples/basic_example.py

run-async:
	python examples/async_example.py

# Development workflow
dev: dev-install format lint test
	@echo "✅ Development setup complete and all checks passed!"
