"""Tests for utility functions."""

import pytest

from mkebook.utils.helpers import (
    chunk_text,
    format_file_size,
    sanitize_filename,
    validate_language_code,
)


class TestFormatFileSize:
    """Tests for format_file_size function."""

    def test_bytes(self) -> None:
        """Test formatting bytes."""
        assert format_file_size(500) == "500.0 B"

    def test_kilobytes(self) -> None:
        """Test formatting kilobytes."""
        assert format_file_size(1024) == "1.0 KB"
        assert format_file_size(1536) == "1.5 KB"

    def test_megabytes(self) -> None:
        """Test formatting megabytes."""
        assert format_file_size(1024 * 1024) == "1.0 MB"
        assert format_file_size(1024 * 1024 * 2) == "2.0 MB"

    def test_gigabytes(self) -> None:
        """Test formatting gigabytes."""
        assert format_file_size(1024 * 1024 * 1024) == "1.0 GB"


class TestValidateLanguageCode:
    """Tests for validate_language_code function."""

    def test_valid_two_letter_codes(self) -> None:
        """Test valid 2-letter language codes."""
        assert validate_language_code("en") is True
        assert validate_language_code("es") is True
        assert validate_language_code("fr") is True

    def test_valid_with_region(self) -> None:
        """Test valid language codes with region."""
        assert validate_language_code("en-US") is True
        assert validate_language_code("zh-CN") is True

    def test_auto_detection(self) -> None:
        """Test auto language detection code."""
        assert validate_language_code("auto") is True

    def test_invalid_codes(self) -> None:
        """Test invalid language codes."""
        assert validate_language_code("eng") is False
        assert validate_language_code("e") is False
        assert validate_language_code("EN") is False
        assert validate_language_code("en-us") is False


class TestSanitizeFilename:
    """Tests for sanitize_filename function."""

    def test_valid_filename(self) -> None:
        """Test that valid filenames are unchanged."""
        assert sanitize_filename("document.txt") == "document.txt"
        assert sanitize_filename("my_file.pdf") == "my_file.pdf"

    def test_remove_invalid_characters(self) -> None:
        """Test removal of invalid characters."""
        assert sanitize_filename("file<name>.txt") == "file_name_.txt"
        assert sanitize_filename('file:name"test') == "file_name_test"

    def test_strip_spaces_and_dots(self) -> None:
        """Test stripping leading/trailing spaces and dots."""
        assert sanitize_filename("  file.txt  ") == "file.txt"
        assert sanitize_filename("...file.txt...") == "file.txt"

    def test_empty_filename(self) -> None:
        """Test handling of empty filename."""
        assert sanitize_filename("") == "unnamed"
        assert sanitize_filename("   ") == "unnamed"

    def test_long_filename(self) -> None:
        """Test truncation of long filenames."""
        long_name = "a" * 300 + ".txt"
        result = sanitize_filename(long_name)
        assert len(result) <= 255
        assert result.endswith(".txt")


class TestChunkText:
    """Tests for chunk_text function."""

    def test_short_text(self) -> None:
        """Test that short text is not chunked."""
        text = "This is a short text."
        chunks = chunk_text(text, max_chunk_size=100)
        assert len(chunks) == 1
        assert chunks[0] == text

    def test_chunk_by_paragraphs(self) -> None:
        """Test chunking by paragraphs."""
        text = "Paragraph 1\n\nParagraph 2\n\nParagraph 3"
        chunks = chunk_text(text, max_chunk_size=20)
        assert len(chunks) > 1

    def test_chunk_large_paragraph(self) -> None:
        """Test chunking of large paragraphs by sentences."""
        text = "Sentence one. Sentence two. Sentence three. Sentence four."
        chunks = chunk_text(text, max_chunk_size=30)
        assert len(chunks) > 1

    def test_preserve_content(self) -> None:
        """Test that all content is preserved after chunking."""
        text = "Para 1\n\nPara 2\n\nPara 3\n\nPara 4"
        chunks = chunk_text(text, max_chunk_size=15)
        combined = " ".join(chunks)
        # Check that key content is preserved
        assert "Para 1" in combined
        assert "Para 2" in combined
        assert "Para 3" in combined
        assert "Para 4" in combined

# Made with Bob
