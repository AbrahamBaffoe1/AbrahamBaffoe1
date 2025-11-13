"""Tests for language detection."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.language_detector import LanguageDetector


def test_detect_by_extension():
    """Test language detection by file extension."""
    assert LanguageDetector.detect_by_extension("code.py") == "python"
    assert LanguageDetector.detect_by_extension("script.js") == "javascript"
    assert LanguageDetector.detect_by_extension("main.go") == "go"
    assert LanguageDetector.detect_by_extension("lib.rs") == "rust"
    assert LanguageDetector.detect_by_extension("types.ts") == "typescript"
    assert LanguageDetector.detect_by_extension("unknown.xyz") == "unknown"


def test_detect_by_content_python():
    """Test Python code detection by content."""
    python_code = '''
import sys
from pathlib import Path

def hello():
    print("Hello")
'''
    assert LanguageDetector.detect_by_content(python_code) == "python"


def test_detect_by_content_javascript():
    """Test JavaScript code detection by content."""
    js_code = '''
const x = 5;
function test() {
    let result = x * 2;
    return result;
}
'''
    assert LanguageDetector.detect_by_content(js_code) == "javascript"


def test_detect_by_content_go():
    """Test Go code detection by content."""
    go_code = '''
package main

func main() {
    fmt.Println("Hello")
}
'''
    assert LanguageDetector.detect_by_content(go_code) == "go"


def test_get_language_info():
    """Test getting language information."""
    python_info = LanguageDetector.get_language_info("python")
    assert python_info["name"] == "Python"
    assert python_info["icon"] == "🐍"

    js_info = LanguageDetector.get_language_info("javascript")
    assert js_info["icon"] == "📜"

    go_info = LanguageDetector.get_language_info("go")
    assert go_info["icon"] == "🐹"


if __name__ == "__main__":
    test_detect_by_extension()
    test_detect_by_content_python()
    test_detect_by_content_javascript()
    test_detect_by_content_go()
    test_get_language_info()
    print("✅ All language detector tests passed!")
