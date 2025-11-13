"""Tests for data models."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.models import CodeReviewFinding, AgentReview, CodeReviewReport


def test_code_review_finding():
    """Test CodeReviewFinding model."""
    finding = CodeReviewFinding(
        severity="high",
        category="security",
        line_number=42,
        code_snippet="eval(user_input)",
        description="Using eval() on untrusted input",
        recommendation="Use json.loads() or ast.literal_eval() instead",
        agent="Security"
    )

    assert finding.severity == "high"
    assert finding.category == "security"
    assert finding.line_number == 42
    assert finding.agent == "Security"


def test_agent_review():
    """Test AgentReview model."""
    finding1 = CodeReviewFinding(
        severity="critical",
        category="security",
        line_number=10,
        code_snippet=None,
        description="SQL injection vulnerability",
        recommendation="Use parameterized queries",
        agent="Security"
    )

    review = AgentReview(
        agent_name="Security",
        findings=[finding1],
        summary="Found critical security issues"
    )

    assert review.agent_name == "Security"
    assert len(review.findings) == 1
    assert review.findings[0].severity == "critical"


def test_code_review_report():
    """Test CodeReviewReport model."""
    report = CodeReviewReport(
        file_name="test.py",
        total_issues=5,
        critical_count=1,
        high_count=2,
        medium_count=2,
        low_count=0,
        info_count=0,
        consolidated_summary="Found 5 issues",
        top_recommendations=["Use parameterized queries", "Remove eval()"]
    )

    assert report.file_name == "test.py"
    assert report.total_issues == 5
    assert report.critical_count == 1
    assert len(report.top_recommendations) == 2


if __name__ == "__main__":
    test_code_review_finding()
    test_agent_review()
    test_code_review_report()
    print("✅ All model tests passed!")
