"""Pytest configuration and fixtures."""

from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    """Provide a temporary directory for tests.

    Args:
        tmp_path: Pytest's temporary directory fixture

    Returns:
        Path to temporary directory
    """
    return tmp_path


@pytest.fixture
def sample_text_file(temp_dir: Path) -> Path:
    """Create a sample text file for testing.

    Args:
        temp_dir: Temporary directory fixture

    Returns:
        Path to the created sample file
    """
    file_path = temp_dir / "sample.txt"
    content = """Chapter 1: Introduction

This is a sample text file for testing the mkebook package.
It contains multiple paragraphs and chapters.

Chapter 2: Content

Here is some more content to test with.
This will be used for creating and translating ebooks.

The End."""

    file_path.write_text(content, encoding="utf-8")
    return file_path


@pytest.fixture
def sample_epub_file(temp_dir: Path) -> Generator[Path, None, None]:
    """Create a sample EPUB file for testing.

    Args:
        temp_dir: Temporary directory fixture

    Yields:
        Path to the created sample EPUB file
    """
    # This is a placeholder - actual EPUB creation would require ebooklib
    file_path = temp_dir / "sample.epub"
    file_path.touch()
    yield file_path
    # Cleanup is automatic with tmp_path


@pytest.fixture
def mock_translation_response() -> str:
    """Provide a mock translation response.

    Returns:
        Mock translated text
    """
    return "Translated text content"

# Made with Bob
