"""Agent orchestrator that coordinates multiple review agents."""

from typing import Optional
from .models import CodeReviewReport, AgentReview
from .agent import ReviewAgent


class CodeReviewOrchestrator:
    """Coordinates multiple agents for comprehensive code review."""

    def __init__(self):
        self.agents: dict[str, ReviewAgent] = {}

    def register_agent(self, agent: ReviewAgent) -> None:
        """Register a code review agent."""
        self.agents[agent.name] = agent

    def review_code(self, code: str, file_path: str) -> CodeReviewReport:
        """
        Run all registered agents on the code and generate a report.

        Args:
            code: Source code to review
            file_path: Path to the file

        Returns:
            Consolidated CodeReviewReport
        """
        # Run all agents in parallel (sequentially for now, can optimize)
        agent_reviews: dict[str, AgentReview] = {}
        all_findings = []

        for agent_name, agent in self.agents.items():
            review = agent.analyze_code(code, file_path)
            agent_reviews[agent_name] = review
            all_findings.extend(review.findings)

        # Count severity levels
        severity_counts = {
            "critical": sum(1 for f in all_findings if f.severity == "critical"),
            "high": sum(1 for f in all_findings if f.severity == "high"),
            "medium": sum(1 for f in all_findings if f.severity == "medium"),
            "low": sum(1 for f in all_findings if f.severity == "low"),
            "info": sum(1 for f in all_findings if f.severity == "info"),
        }

        # Sort findings by severity
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
        sorted_findings = sorted(
            all_findings, key=lambda f: (severity_order.get(f.severity, 5), f.line_number or 0)
        )

        # Top recommendations from critical/high findings
        top_recommendations = []
        for finding in sorted_findings[:5]:  # Top 5 recommendations
            if finding.recommendation and finding.recommendation not in top_recommendations:
                top_recommendations.append(finding.recommendation)

        # Build consolidated summary
        consolidated_summary = self._build_summary(agent_reviews, severity_counts)

        report = CodeReviewReport(
            file_name=file_path,
            total_issues=len(all_findings),
            critical_count=severity_counts["critical"],
            high_count=severity_counts["high"],
            medium_count=severity_counts["medium"],
            low_count=severity_counts["low"],
            info_count=severity_counts["info"],
            agent_reviews=agent_reviews,
            consolidated_summary=consolidated_summary,
            top_recommendations=top_recommendations,
        )

        return report

    def _build_summary(self, agent_reviews: dict[str, AgentReview], severity_counts: dict) -> str:
        """Build a consolidated summary from all agent reviews."""
        summary_parts = [
            f"Code Review Summary for {self._extract_filename(agent_reviews)}:",
            f"- Total Issues Found: {severity_counts['critical'] + severity_counts['high'] + severity_counts['medium'] + severity_counts['low'] + severity_counts['info']}",
            f"  - Critical: {severity_counts['critical']}",
            f"  - High: {severity_counts['high']}",
            f"  - Medium: {severity_counts['medium']}",
            f"  - Low: {severity_counts['low']}",
            f"  - Info: {severity_counts['info']}",
            "",
            "Agent Reviews:",
        ]

        for agent_name, review in agent_reviews.items():
            if review.summary:
                summary_parts.append(f"- {agent_name}: {review.summary}")

        return "\n".join(summary_parts)

    def _extract_filename(self, agent_reviews: dict[str, AgentReview]) -> str:
        """Extract filename from first agent review."""
        if agent_reviews:
            first_review = next(iter(agent_reviews.values()))
            if first_review.findings:
                return first_review.findings[0].agent
        return "Unknown File"
