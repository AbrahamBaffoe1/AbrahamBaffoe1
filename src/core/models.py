"""Data models for the multi-agent code review system."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CodeReviewFinding:
    """Represents a single finding from a code review."""

    severity: str  # "critical", "high", "medium", "low", "info"
    category: str  # e.g., "security", "performance", "style"
    line_number: Optional[int]
    code_snippet: Optional[str]
    description: str
    recommendation: str
    agent: str  # which agent found this


@dataclass
class AgentReview:
    """Output from a single review agent."""

    agent_name: str
    findings: list[CodeReviewFinding] = field(default_factory=list)
    summary: str = ""
    thinking_process: str = ""


@dataclass
class CodeReviewReport:
    """Final consolidated code review report."""

    file_name: str
    total_issues: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    info_count: int

    agent_reviews: dict[str, AgentReview] = field(default_factory=dict)
    consolidated_summary: str = ""

    # Recommendations ranked by impact
    top_recommendations: list[str] = field(default_factory=list)
