"""Web dashboard for visualizing code review results."""

import json
from typing import Optional

try:
    from flask import Flask, render_string, request, jsonify
except ImportError:
    Flask = None
    render_string = None
    request = None
    jsonify = None

from .analyzer import CodeReviewAnalyzer


def create_dashboard_app(analyzer: Optional[CodeReviewAnalyzer] = None) -> Flask:
    """
    Create a Flask app for the code review dashboard.

    Args:
        analyzer: CodeReviewAnalyzer instance (creates new if None)

    Returns:
        Flask application
    """
    if Flask is None:
        raise ImportError("Flask is required for the dashboard")

    app = Flask(__name__)
    analyzer = analyzer or CodeReviewAnalyzer()

    @app.route("/", methods=["GET"])
    def index():
        """Main dashboard page."""
        return render_string(get_index_html())

    @app.route("/api/analyze", methods=["POST"])
    def analyze():
        """API endpoint to analyze code or file."""
        data = request.get_json()
        code = data.get("code")
        file_path = data.get("file_path", "code.py")

        if not code:
            return jsonify({"error": "No code provided"}), 400

        try:
            result = analyzer.analyze_file_by_content(code, file_path)
            return jsonify({"status": "success", "result": result}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/analyze-file", methods=["POST"])
    def analyze_file():
        """API endpoint to analyze a file path."""
        data = request.get_json()
        file_path = data.get("file_path")

        if not file_path:
            return jsonify({"error": "No file path provided"}), 400

        try:
            result = analyzer.analyze_file(file_path)
            return jsonify({"status": "success", "result": result}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app


def get_index_html() -> str:
    """Get the HTML for the dashboard."""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Agentic Code Reviewer Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
                         'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
                         sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }

        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
        }

        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        header p {
            font-size: 1.1em;
            opacity: 0.9;
        }

        .content {
            padding: 40px;
        }

        .upload-section {
            margin-bottom: 40px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }

        textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
            font-size: 13px;
            resize: vertical;
            min-height: 200px;
        }

        textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        input[type="text"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            font-size: 14px;
        }

        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }

        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }

        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .results-section {
            display: none;
        }

        .results-section.active {
            display: block;
        }

        .summary {
            background: #f5f7fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            border-left: 4px solid #667eea;
        }

        .summary h2 {
            color: #333;
            margin-bottom: 15px;
        }

        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }

        .metric {
            background: white;
            padding: 15px;
            border-radius: 6px;
            text-align: center;
        }

        .metric-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }

        .metric-label {
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }

        .metric.critical .metric-value { color: #ef4444; }
        .metric.high .metric-value { color: #f97316; }
        .metric.medium .metric-value { color: #eab308; }
        .metric.low .metric-value { color: #22c55e; }

        .charts {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }

        .chart-container {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            position: relative;
            height: 300px;
        }

        .chart-container canvas {
            position: absolute;
            top: 0;
            left: 0;
        }

        .findings {
            margin-top: 30px;
        }

        .findings h2 {
            color: #333;
            margin-bottom: 20px;
        }

        .agent-section {
            margin-bottom: 30px;
        }

        .agent-header {
            background: #f5f7fa;
            padding: 12px 16px;
            border-radius: 6px;
            margin-bottom: 12px;
            font-weight: 600;
            color: #333;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .agent-icon {
            font-size: 1.2em;
        }

        .finding {
            background: white;
            padding: 16px;
            border-radius: 6px;
            margin-bottom: 12px;
            border-left: 4px solid #e0e0e0;
        }

        .finding.critical { border-left-color: #ef4444; background: #fef2f2; }
        .finding.high { border-left-color: #f97316; background: #fff7ed; }
        .finding.medium { border-left-color: #eab308; background: #fffbeb; }
        .finding.low { border-left-color: #22c55e; background: #f0fdf4; }

        .finding-severity {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: 600;
            margin-bottom: 8px;
        }

        .severity-critical { background: #ef4444; color: white; }
        .severity-high { background: #f97316; color: white; }
        .severity-medium { background: #eab308; color: black; }
        .severity-low { background: #22c55e; color: white; }

        .finding-description {
            color: #333;
            margin: 10px 0;
        }

        .finding-recommendation {
            background: white;
            padding: 10px;
            border-radius: 4px;
            margin-top: 10px;
            color: #555;
            font-style: italic;
        }

        .error {
            background: #fef2f2;
            border: 2px solid #ef4444;
            color: #991b1b;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }

        .loading {
            text-align: center;
            padding: 40px;
            color: #667eea;
        }

        .spinner {
            border: 4px solid #f0f0f0;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        footer {
            background: #f5f7fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #e0e0e0;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🤖 Agentic Code Reviewer</h1>
            <p>Multi-agent AI system for comprehensive code analysis</p>
        </header>

        <div class="content">
            <div class="upload-section">
                <div class="form-group">
                    <label for="file-path">File Path (or name for reference):</label>
                    <input type="text" id="file-path" placeholder="e.g., app.py" value="code.py">
                </div>

                <div class="form-group">
                    <label for="code-input">Paste your code here:</label>
                    <textarea id="code-input" placeholder="Paste your Python, JavaScript, Go, or Rust code..."></textarea>
                </div>

                <button onclick="analyzeCode()" id="analyze-btn">🔍 Analyze Code</button>
            </div>

            <div class="results-section" id="results">
                <div class="loading" id="loading" style="display: none;">
                    <div class="spinner"></div>
                    <p>Analyzing code with 4 specialized agents...</p>
                </div>

                <div id="results-content" style="display: none;">
                    <div class="summary">
                        <h2>📊 Analysis Summary</h2>
                        <div class="metrics" id="metrics"></div>
                    </div>

                    <div class="charts">
                        <div class="chart-container">
                            <canvas id="severityChart"></canvas>
                        </div>
                        <div class="chart-container">
                            <canvas id="agentChart"></canvas>
                        </div>
                    </div>

                    <div class="summary">
                        <h2>💡 Top Recommendations</h2>
                        <div id="recommendations"></div>
                    </div>

                    <div class="findings">
                        <h2>📋 Detailed Findings</h2>
                        <div id="findings"></div>
                    </div>
                </div>

                <div id="error-message" class="error" style="display: none;"></div>
            </div>
        </div>

        <footer>
            <p>Built with ❤️ using Anthropic's Claude API</p>
        </footer>
    </div>

    <script>
        let severityChart, agentChart;

        async function analyzeCode() {
            const code = document.getElementById('code-input').value;
            const filePath = document.getElementById('file-path').value || 'code.py';

            if (!code.trim()) {
                alert('Please paste some code to analyze');
                return;
            }

            const resultsDiv = document.getElementById('results');
            const loadingDiv = document.getElementById('loading');
            const resultsContent = document.getElementById('results-content');
            const errorDiv = document.getElementById('error-message');

            resultsDiv.classList.add('active');
            loadingDiv.style.display = 'block';
            resultsContent.style.display = 'none';
            errorDiv.style.display = 'none';
            document.getElementById('analyze-btn').disabled = true;

            try {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ code, file_path: filePath })
                });

                if (!response.ok) {
                    throw new Error('Analysis failed');
                }

                const data = await response.json();
                if (data.status === 'success') {
                    displayResults(data.result);
                } else {
                    throw new Error(data.error || 'Unknown error');
                }
            } catch (error) {
                errorDiv.textContent = '❌ Error: ' + error.message;
                errorDiv.style.display = 'block';
            } finally {
                loadingDiv.style.display = 'none';
                document.getElementById('analyze-btn').disabled = false;
            }
        }

        function displayResults(result) {
            // Display metrics
            const metrics = result.severity_breakdown;
            const metricsHtml = `
                <div class="metric critical">
                    <div class="metric-value">${metrics.critical}</div>
                    <div class="metric-label">Critical</div>
                </div>
                <div class="metric high">
                    <div class="metric-value">${metrics.high}</div>
                    <div class="metric-label">High</div>
                </div>
                <div class="metric medium">
                    <div class="metric-value">${metrics.medium}</div>
                    <div class="metric-label">Medium</div>
                </div>
                <div class="metric low">
                    <div class="metric-value">${metrics.low}</div>
                    <div class="metric-label">Low</div>
                </div>
                <div class="metric">
                    <div class="metric-value">${result.total_issues}</div>
                    <div class="metric-label">Total Issues</div>
                </div>
            `;
            document.getElementById('metrics').innerHTML = metricsHtml;

            // Severity chart
            updateSeverityChart(metrics);

            // Agent chart
            updateAgentChart(result.agent_reviews);

            // Recommendations
            const recsHtml = result.top_recommendations
                .map(rec => `<div style="margin-bottom: 10px; padding: 10px; background: white; border-radius: 4px;">✓ ${rec}</div>`)
                .join('');
            document.getElementById('recommendations').innerHTML = recsHtml || '<p>No recommendations</p>';

            // Findings
            displayFindings(result.agent_reviews);

            document.getElementById('results-content').style.display = 'block';
        }

        function updateSeverityChart(metrics) {
            const ctx = document.getElementById('severityChart').getContext('2d');

            if (severityChart) severityChart.destroy();

            severityChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Critical', 'High', 'Medium', 'Low', 'Info'],
                    datasets: [{
                        data: [metrics.critical, metrics.high, metrics.medium, metrics.low, metrics.info],
                        backgroundColor: ['#ef4444', '#f97316', '#eab308', '#22c55e', '#3b82f6'],
                        borderColor: 'white',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'bottom' },
                        title: { display: true, text: 'Issues by Severity' }
                    }
                }
            });
        }

        function updateAgentChart(agentReviews) {
            const ctx = document.getElementById('agentChart').getContext('2d');
            const agentNames = Object.keys(agentReviews);
            const issueCounts = agentNames.map(name => agentReviews[name].findings.length);

            if (agentChart) agentChart.destroy();

            agentChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: agentNames,
                    datasets: [{
                        label: 'Issues Found',
                        data: issueCounts,
                        backgroundColor: '#667eea',
                        borderRadius: 6,
                        borderSkipped: false
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    indexAxis: 'y',
                    plugins: {
                        legend: { display: false },
                        title: { display: true, text: 'Issues by Agent' }
                    }
                }
            });
        }

        function displayFindings(agentReviews) {
            const agentIcons = {
                'Security': '🔐',
                'Performance': '⚡',
                'Style': '🎨',
                'Architecture': '🏗️'
            };

            let findingsHtml = '';
            for (const [agentName, review] of Object.entries(agentReviews)) {
                if (review.findings.length === 0) continue;

                findingsHtml += `
                    <div class="agent-section">
                        <div class="agent-header">
                            <span class="agent-icon">${agentIcons[agentName] || '🤖'}</span>
                            ${agentName} (${review.findings.length} issues)
                        </div>
                `;

                for (const finding of review.findings) {
                    findingsHtml += `
                        <div class="finding ${finding.severity}">
                            <div class="finding-severity severity-${finding.severity}">
                                ${finding.severity.toUpperCase()}
                            </div>
                            <div class="finding-description">
                                <strong>Line ${finding.line_number || 'N/A'}:</strong> ${finding.description}
                            </div>
                            <div class="finding-recommendation">
                                💡 ${finding.recommendation}
                            </div>
                        </div>
                    `;
                }

                findingsHtml += '</div>';
            }

            document.getElementById('findings').innerHTML = findingsHtml || '<p>No findings</p>';
        }

        // Allow Enter to analyze
        document.getElementById('code-input').addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') analyzeCode();
        });
    </script>
</body>
</html>
"""
