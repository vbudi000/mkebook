"""Tests for ebook creation functionality."""

from pathlib import Path

import pytest

from mkebook.core.ebook import EbookCreator, EbookFormat


class TestEbookFormat:
    """Tests for EbookFormat enum."""

    def test_format_values(self) -> None:
        """Test that format enum has correct values."""
        assert EbookFormat.EPUB.value == "epub"
        assert EbookFormat.PDF.value == "pdf"
        assert EbookFormat.MOBI.value == "mobi"
        assert EbookFormat.TXT.value == "txt"


class TestEbookCreator:
    """Tests for EbookCreator class."""

    def test_initialization(self) -> None:
        """Test EbookCreator initialization."""
        creator = EbookCreator()
        assert creator is not None
        assert len(creator.supported_formats) == 4

    def test_create_txt_ebook(self, sample_text_file: Path, temp_dir: Path) -> None:
        """Test creating a plain text ebook."""
        creator = EbookCreator()
        output_file = temp_dir / "output.txt"

        creator.create(
            input_file=sample_text_file,
            output_file=output_file,
            format=EbookFormat.TXT,
            title="Test Book",
        )

        assert output_file.exists()
        content = output_file.read_text(encoding="utf-8")
        assert len(content) > 0

    def test_create_with_missing_input(self, temp_dir: Path) -> None:
        """Test that creating ebook with missing input raises error."""
        creator = EbookCreator()
        input_file = temp_dir / "nonexistent.txt"
        output_file = temp_dir / "output.epub"

        with pytest.raises(FileNotFoundError):
            creator.create(
                input_file=input_file,
                output_file=output_file,
                format=EbookFormat.EPUB,
            )

    def test_read_input(self, sample_text_file: Path) -> None:
        """Test reading input file."""
        creator = EbookCreator()
        content = creator._read_input(sample_text_file)

        assert isinstance(content, str)
        assert len(content) > 0
        assert "Chapter 1" in content

    def test_text_to_html(self) -> None:
        """Test converting text to HTML."""
        creator = EbookCreator()
        text = "Paragraph 1\n\nParagraph 2\n\nParagraph 3"
        html = creator._text_to_html(text)

        assert "<p>Paragraph 1</p>" in html
        assert "<p>Paragraph 2</p>" in html
        assert "<p>Paragraph 3</p>" in html
        assert "<html>" in html
        assert "</html>" in html

    def test_pdf_not_implemented(self, sample_text_file: Path, temp_dir: Path) -> None:
        """Test that PDF creation raises NotImplementedError."""
        creator = EbookCreator()
        output_file = temp_dir / "output.pdf"

        with pytest.raises(NotImplementedError):
            creator.create(
                input_file=sample_text_file,
                output_file=output_file,
                format=EbookFormat.PDF,
            )

    def test_mobi_not_implemented(self, sample_text_file: Path, temp_dir: Path) -> None:
        """Test that MOBI creation raises NotImplementedError."""
        creator = EbookCreator()
        output_file = temp_dir / "output.mobi"

        with pytest.raises(NotImplementedError):
            creator.create(
                input_file=sample_text_file,
                output_file=output_file,
                format=EbookFormat.MOBI,
            )

# Made with Bob
