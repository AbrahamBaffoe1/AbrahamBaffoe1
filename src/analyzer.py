"""Main analyzer that orchestrates code reviews."""

from pathlib import Path
from .core import CodeReviewOrchestrator
from .agents import SecurityAgent, PerformanceAgent, StyleAgent, ArchitectureAgent


class CodeReviewAnalyzer:
    """High-level analyzer for reviewing code files."""

    def __init__(self):
        self.orchestrator = CodeReviewOrchestrator()
        self._setup_agents()

    def _setup_agents(self) -> None:
        """Register all review agents."""
        self.orchestrator.register_agent(SecurityAgent())
        self.orchestrator.register_agent(PerformanceAgent())
        self.orchestrator.register_agent(StyleAgent())
        self.orchestrator.register_agent(ArchitectureAgent())

    def analyze_file(self, file_path: str) -> dict:
        """
        Analyze a single file.

        Args:
            file_path: Path to the file to analyze

        Returns:
            Dictionary with analysis results
        """
        # Read the file
        with open(file_path, "r") as f:
            code = f.read()

        # Run orchestrator
        report = self.orchestrator.review_code(code, file_path)

        return self._report_to_dict(report)

    def analyze_directory(self, directory: str, pattern: str = "**/*.py") -> dict:
        """
        Analyze all files in a directory.

        Args:
            directory: Path to directory
            pattern: File pattern to match

        Returns:
            Dictionary with analysis results for all files
        """
        path = Path(directory)
        files = list(path.glob(pattern))

        results = {}
        for file in files:
            if file.is_file():
                try:
                    results[str(file)] = self.analyze_file(str(file))
                except Exception as e:
                    results[str(file)] = {"error": str(e)}

        return results

    def _report_to_dict(self, report) -> dict:
        """Convert CodeReviewReport to dictionary."""
        return {
            "file_name": report.file_name,
            "total_issues": report.total_issues,
            "severity_breakdown": {
                "critical": report.critical_count,
                "high": report.high_count,
                "medium": report.medium_count,
                "low": report.low_count,
                "info": report.info_count,
            },
            "consolidated_summary": report.consolidated_summary,
            "top_recommendations": report.top_recommendations,
            "agent_reviews": {
                agent_name: {
                    "findings": [
                        {
                            "severity": f.severity,
                            "category": f.category,
                            "line_number": f.line_number,
                            "description": f.description,
                            "recommendation": f.recommendation,
                        }
                        for f in review.findings
                    ],
                    "summary": review.summary,
                }
                for agent_name, review in report.agent_reviews.items()
            },
        }
