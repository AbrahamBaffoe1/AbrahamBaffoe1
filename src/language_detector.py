"""Detect programming language from file path or code."""

from pathlib import Path


class LanguageDetector:
    """Detects programming language from file extensions and code patterns."""

    LANGUAGE_EXTENSIONS = {
        ".py": "python",
        ".js": "javascript",
        ".jsx": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".go": "go",
        ".rs": "rust",
    }

    @staticmethod
    def detect_by_extension(file_path: str) -> str:
        """
        Detect language by file extension.

        Args:
            file_path: Path to the file

        Returns:
            Language name (python, javascript, go, rust, etc.)
        """
        ext = Path(file_path).suffix.lower()
        return LanguageDetector.LANGUAGE_EXTENSIONS.get(ext, "unknown")

    @staticmethod
    def detect_by_content(code: str, file_path: str = "") -> str:
        """
        Detect language by code content and file path.

        Args:
            code: Source code content
            file_path: Optional file path for extension checking

        Returns:
            Language name
        """
        # Try extension first
        if file_path:
            lang = LanguageDetector.detect_by_extension(file_path)
            if lang != "unknown":
                return lang

        # Detect by content patterns
        if "import " in code and ("from " in code or "import sys" in code):
            return "python"
        elif "function " in code or "const " in code or "let " in code or "var " in code:
            return "javascript"
        elif "func " in code and "package " in code:
            return "go"
        elif "fn " in code and "let " in code:
            return "rust"

        return "unknown"

    @staticmethod
    def get_language_info(language: str) -> dict:
        """
        Get language-specific information.

        Args:
            language: Language name

        Returns:
            Dictionary with language info
        """
        info = {
            "python": {
                "name": "Python",
                "icon": "🐍",
                "indent": "spaces (4)",
                "type_system": "Dynamic",
            },
            "javascript": {
                "name": "JavaScript/TypeScript",
                "icon": "📜",
                "indent": "spaces (2-4)",
                "type_system": "Dynamic/Optional",
            },
            "typescript": {
                "name": "TypeScript",
                "icon": "📘",
                "indent": "spaces (2-4)",
                "type_system": "Static",
            },
            "go": {
                "name": "Go",
                "icon": "🐹",
                "indent": "tabs",
                "type_system": "Static",
            },
            "rust": {
                "name": "Rust",
                "icon": "🦀",
                "indent": "spaces (4)",
                "type_system": "Static",
            },
        }

        return info.get(language, {"name": "Unknown", "icon": "❓"})
