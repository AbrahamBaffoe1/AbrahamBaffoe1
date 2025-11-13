#!/usr/bin/env python3
"""Main application for the Agentic Code Reviewer."""

import os
from dotenv import load_dotenv

load_dotenv()

from src.web_dashboard import create_dashboard_app

if __name__ == "__main__":
    app = create_dashboard_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
