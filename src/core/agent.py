"""Base agent framework for code review agents."""

import asyncio
import json
from abc import ABC, abstractmethod
from typing import Optional

from anthropic import Anthropic, AsyncAnthropic

from .models import AgentReview, CodeReviewFinding


class ReviewAgent(ABC):
    """Base class for all code review agents."""

    def __init__(self, name: str, model: str = "claude-3-5-sonnet-20241022"):
        self.name = name
        self.model = model
        self.client = Anthropic()
        self.async_client = AsyncAnthropic()

    @abstractmethod
    def get_system_prompt(self, language: str = "python") -> str:
        """
        Return the system prompt that defines this agent's role.

        Args:
            language: Programming language being analyzed

        Returns:
            System prompt for the agent
        """
        pass

    def analyze_code(self, code: str, file_path: str) -> AgentReview:
        """
        Analyze code and return findings.

        Args:
            code: The source code to analyze
            file_path: Path to the file being analyzed

        Returns:
            AgentReview with findings and analysis
        """
        # Detect language
        from ..language_detector import LanguageDetector

        language = LanguageDetector.detect_by_content(code, file_path)
        system_prompt = self.get_system_prompt(language)

        user_message = f"""Analyze this code for {self.name.lower()} issues:

File: {file_path}

```
{code}
```

Respond ONLY with valid JSON (no markdown, no code blocks) in this format:
{{
  "findings": [
    {{
      "severity": "critical|high|medium|low|info",
      "line_number": <line_number or null>,
      "code_snippet": "<snippet or null>",
      "description": "<what's wrong>",
      "recommendation": "<how to fix it>"
    }}
  ],
  "summary": "<overall assessment>"
}}"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )

        response_text = response.content[0].text
        result = json.loads(response_text)

        findings = [
            CodeReviewFinding(
                severity=f["severity"],
                category=self.name.lower(),
                line_number=f.get("line_number"),
                code_snippet=f.get("code_snippet"),
                description=f["description"],
                recommendation=f["recommendation"],
                agent=self.name,
            )
            for f in result.get("findings", [])
        ]

        return AgentReview(
            agent_name=self.name,
            findings=findings,
            summary=result.get("summary", ""),
            thinking_process="",
        )

    async def analyze_code_async(self, code: str, file_path: str) -> AgentReview:
        """
        Analyze code asynchronously and return findings.

        Args:
            code: The source code to analyze
            file_path: Path to the file being analyzed

        Returns:
            AgentReview with findings and analysis
        """
        # Detect language
        from ..language_detector import LanguageDetector

        language = LanguageDetector.detect_by_content(code, file_path)
        system_prompt = self.get_system_prompt(language)

        user_message = f"""Analyze this code for {self.name.lower()} issues:

File: {file_path}

```
{code}
```

Respond ONLY with valid JSON (no markdown, no code blocks) in this format:
{{
  "findings": [
    {{
      "severity": "critical|high|medium|low|info",
      "line_number": <line_number or null>,
      "code_snippet": "<snippet or null>",
      "description": "<what's wrong>",
      "recommendation": "<how to fix it>"
    }}
  ],
  "summary": "<overall assessment>"
}}"""

        response = await self.async_client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )

        response_text = response.content[0].text
        result = json.loads(response_text)

        findings = [
            CodeReviewFinding(
                severity=f["severity"],
                category=self.name.lower(),
                line_number=f.get("line_number"),
                code_snippet=f.get("code_snippet"),
                description=f["description"],
                recommendation=f["recommendation"],
                agent=self.name,
            )
            for f in result.get("findings", [])
        ]

        return AgentReview(
            agent_name=self.name,
            findings=findings,
            summary=result.get("summary", ""),
            thinking_process="",
        )
