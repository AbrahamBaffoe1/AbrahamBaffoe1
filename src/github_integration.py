"""GitHub integration for automatic PR code reviews."""

import hmac
import hashlib
import json
import os
from typing import Optional

try:
    import requests
    from flask import Flask, request, jsonify
except ImportError:
    requests = None
    Flask = None
    request = None
    jsonify = None

from .analyzer import CodeReviewAnalyzer


class GitHubPRReviewer:
    """Handles automatic code review of GitHub Pull Requests."""

    def __init__(self, github_token: str, analyzer: Optional[CodeReviewAnalyzer] = None):
        """
        Initialize GitHub PR reviewer.

        Args:
            github_token: GitHub personal access token
            analyzer: CodeReviewAnalyzer instance (creates new if None)
        """
        self.github_token = github_token
        self.analyzer = analyzer or CodeReviewAnalyzer()
        self.api_base = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
        }

    def review_pr(self, owner: str, repo: str, pr_number: int) -> dict:
        """
        Review a pull request and post comments.

        Args:
            owner: Repository owner
            repo: Repository name
            pr_number: PR number

        Returns:
            Dictionary with review results
        """
        # Get PR details
        pr_url = f"{self.api_base}/repos/{owner}/{repo}/pulls/{pr_number}"
        pr_response = requests.get(pr_url, headers=self.headers)
        pr_data = pr_response.json()

        # Get changed files
        files_url = f"{self.api_base}/repos/{owner}/{repo}/pulls/{pr_number}/files"
        files_response = requests.get(files_url, headers=self.headers)
        files_data = files_response.json()

        results = {}

        # Review each changed file
        for file_info in files_data:
            file_path = file_info["filename"]
            if not self._should_review_file(file_path):
                continue

            # Get file content
            file_url = file_info["contents_url"]
            file_response = requests.get(file_url, headers=self.headers)
            if file_response.status_code != 200:
                continue

            file_content = file_response.json().get("content", "")
            import base64

            try:
                code = base64.b64decode(file_content).decode("utf-8")
            except Exception:
                continue

            # Analyze code
            analysis = self.analyzer.analyze_file_by_content(code, file_path)

            if analysis and analysis.get("total_issues", 0) > 0:
                results[file_path] = analysis
                self._post_comments(owner, repo, pr_number, file_path, file_info, analysis)

        return {"reviewed_files": len(results), "files_with_issues": results}

    def _should_review_file(self, file_path: str) -> bool:
        """Check if file should be reviewed."""
        python_extensions = {".py"}
        js_extensions = {".js", ".ts", ".jsx", ".tsx"}
        go_extensions = {".go"}
        rust_extensions = {".rs"}

        ext = "." + file_path.split(".")[-1] if "." in file_path else ""
        return ext in (python_extensions | js_extensions | go_extensions | rust_extensions)

    def _post_comments(
        self, owner: str, repo: str, pr_number: int, file_path: str, file_info: dict, analysis: dict
    ) -> None:
        """Post review comments on the PR."""
        critical_issues = []
        high_issues = []

        for agent_name, review in analysis.get("agent_reviews", {}).items():
            for finding in review.get("findings", []):
                if finding["severity"] == "critical":
                    critical_issues.append(
                        f"**{agent_name}** ({finding['category']}): {finding['description']}"
                    )
                elif finding["severity"] == "high":
                    high_issues.append(
                        f"**{agent_name}** ({finding['category']}): {finding['description']}"
                    )

        if not critical_issues and not high_issues:
            return

        # Create comment body
        comment_body = f"## 🤖 Agentic Code Review\n\n**File**: `{file_path}`\n\n"

        if critical_issues:
            comment_body += "### 🔴 Critical Issues\n"
            for issue in critical_issues[:5]:
                comment_body += f"- {issue}\n"

        if high_issues:
            comment_body += "\n### 🟠 High Priority Issues\n"
            for issue in high_issues[:5]:
                comment_body += f"- {issue}\n"

        comment_body += f"\n**Total Issues**: {analysis['total_issues']}\n"
        comment_body += (
            f"**Breakdown**: {analysis['severity_breakdown']['critical']} critical, "
            f"{analysis['severity_breakdown']['high']} high, "
            f"{analysis['severity_breakdown']['medium']} medium\n"
        )

        # Post review comment
        comments_url = f"{self.api_base}/repos/{owner}/{repo}/issues/{pr_number}/comments"
        requests.post(comments_url, headers=self.headers, json={"body": comment_body})

    def verify_webhook_signature(self, payload: bytes, signature: str, secret: str) -> bool:
        """
        Verify GitHub webhook signature.

        Args:
            payload: Webhook payload bytes
            signature: X-Hub-Signature header value
            secret: Webhook secret

        Returns:
            True if signature is valid
        """
        expected_signature = "sha256=" + hmac.new(
            secret.encode(), payload, hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(signature, expected_signature)


def create_webhook_handler(github_token: str, webhook_secret: str) -> Flask:
    """
    Create a Flask app for handling GitHub webhooks.

    Args:
        github_token: GitHub personal access token
        webhook_secret: Webhook secret for signature verification

    Returns:
        Flask application
    """
    if Flask is None:
        raise ImportError("Flask is required for webhook handling")

    app = Flask(__name__)
    reviewer = GitHubPRReviewer(github_token)

    @app.route("/webhook", methods=["POST"])
    def webhook():
        """Handle GitHub webhook."""
        # Verify signature
        signature = request.headers.get("X-Hub-Signature-256", "")
        if not reviewer.verify_webhook_signature(request.data, signature, webhook_secret):
            return jsonify({"error": "Invalid signature"}), 401

        # Parse payload
        payload = request.get_json()
        action = payload.get("action")

        # Only review on PR open or synchronize
        if action not in ("opened", "synchronize"):
            return jsonify({"status": "ignored"}), 200

        pr = payload.get("pull_request", {})
        if not pr:
            return jsonify({"error": "No PR data"}), 400

        owner = payload["repository"]["owner"]["login"]
        repo = payload["repository"]["name"]
        pr_number = pr["number"]

        # Review PR
        try:
            result = reviewer.review_pr(owner, repo, pr_number)
            return jsonify({"status": "success", "result": result}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app
