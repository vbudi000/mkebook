"""Ebook creation and manipulation functionality."""

from enum import Enum
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup
from ebooklib import epub
from rich.console import Console

console = Console()


class EbookFormat(Enum):
    """Supported ebook formats."""

    EPUB = "epub"
    PDF = "pdf"
    MOBI = "mobi"
    TXT = "txt"


class EbookCreator:
    """Create ebooks from various input formats."""

    def __init__(self) -> None:
        """Initialize the ebook creator."""
        self.supported_formats = [fmt.value for fmt in EbookFormat]

    def create(
        self,
        input_file: Path,
        output_file: Path,
        format: EbookFormat = EbookFormat.EPUB,
        title: Optional[str] = None,
        author: Optional[str] = None,
        language: str = "en",
    ) -> None:
        """Create an ebook from an input file.

        Args:
            input_file: Path to the source file
            output_file: Path where the ebook will be saved
            format: Output format for the ebook
            title: Title of the ebook (defaults to filename)
            author: Author of the ebook
            language: Language code (e.g., 'en', 'es', 'fr')

        Raises:
            ValueError: If the format is not supported
            FileNotFoundError: If the input file doesn't exist
        """
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")

        if format not in EbookFormat:
            raise ValueError(f"Unsupported format: {format}")

        # Use filename as title if not provided
        if title is None:
            title = input_file.stem

        # Read input content
        content = self._read_input(input_file)

        # Create ebook based on format
        if format == EbookFormat.EPUB:
            self._create_epub(output_file, content, title, author, language)
        elif format == EbookFormat.PDF:
            self._create_pdf(output_file, content, title, author)
        elif format == EbookFormat.MOBI:
            self._create_mobi(output_file, content, title, author)
        elif format == EbookFormat.TXT:
            self._create_txt(output_file, content)

    def _read_input(self, input_file: Path) -> str:
        """Read content from input file.

        Args:
            input_file: Path to the input file

        Returns:
            Content of the file as string
        """
        with open(input_file, "r", encoding="utf-8") as f:
            return f.read()

    def _create_epub(
        self,
        output_file: Path,
        content: str,
        title: str,
        author: Optional[str],
        language: str,
    ) -> None:
        """Create an EPUB ebook.

        Args:
            output_file: Path where the EPUB will be saved
            content: Content to include in the ebook
            title: Title of the ebook
            author: Author of the ebook
            language: Language code
        """
        book = epub.EpubBook()

        # Set metadata
        book.set_identifier(f"mkebook_{title.replace(' ', '_')}")
        book.set_title(title)
        book.set_language(language)

        if author:
            book.add_author(author)

        # Create chapter
        chapter = epub.EpubHtml(
            title="Chapter 1",
            file_name="chap_01.xhtml",
            lang=language,
        )

        # Convert content to HTML if needed
        html_content = self._text_to_html(content)
        chapter.content = html_content

        # Add chapter to book
        book.add_item(chapter)

        # Define Table of Contents
        book.toc = (chapter,)

        # Add navigation files
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # Define spine
        book.spine = ["nav", chapter]

        # Write EPUB file
        epub.write_epub(str(output_file), book)

    def create_from_chapters(
        self,
        chapters: list[tuple[str, str]],
        output_file: Path,
        title: str,
        author: Optional[str] = None,
        language: str = "en",
    ) -> None:
        """Create an EPUB ebook from multiple chapters.

        Args:
            chapters: List of tuples containing (chapter_title, chapter_content)
            output_file: Path where the EPUB will be saved
            title: Title of the ebook
            author: Author of the ebook
            language: Language code
        """
        console.print(f"[blue]Creating EPUB with {len(chapters)} chapters...[/blue]")
        
        book = epub.EpubBook()

        # Set metadata
        book.set_identifier(f"mkebook_{title.replace(' ', '_')}")
        book.set_title(title)
        book.set_language(language)

        if author:
            book.add_author(author)

        # Create chapters
        epub_chapters = []
        toc_entries = []
        
        for idx, (chapter_title, chapter_content) in enumerate(chapters, 1):
            chapter = epub.EpubHtml(
                title=chapter_title,
                file_name=f"chap_{idx:04d}.xhtml",
                lang=language,
            )

            # Convert content to HTML
            html_content = self._text_to_html(chapter_content)
            chapter.content = html_content

            # Add chapter to book
            book.add_item(chapter)
            epub_chapters.append(chapter)
            toc_entries.append(chapter)

        # Define Table of Contents
        book.toc = tuple(toc_entries)

        # Add navigation files
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # Define spine
        book.spine = ["nav"] + epub_chapters

        # Write EPUB file
        epub.write_epub(str(output_file), book)
        console.print(f"[green]✓ EPUB created successfully: {output_file}[/green]")

    def _create_pdf(
        self,
        output_file: Path,
        content: str,
        title: str,
        author: Optional[str],
    ) -> None:
        """Create a PDF ebook.

        Args:
            output_file: Path where the PDF will be saved
            content: Content to include in the ebook
            title: Title of the ebook
            author: Author of the ebook

        Note:
            This is a placeholder. PDF generation requires additional libraries
            like reportlab or weasyprint.
        """
        # TODO: Implement PDF generation
        raise NotImplementedError("PDF generation is not yet implemented")

    def _create_mobi(
        self,
        output_file: Path,
        content: str,
        title: str,
        author: Optional[str],
    ) -> None:
        """Create a MOBI ebook.

        Args:
            output_file: Path where the MOBI will be saved
            content: Content to include in the ebook
            title: Title of the ebook
            author: Author of the ebook

        Note:
            This is a placeholder. MOBI generation typically requires
            converting from EPUB using Calibre's ebook-convert tool.
        """
        # TODO: Implement MOBI generation
        raise NotImplementedError("MOBI generation is not yet implemented")

    def _create_txt(self, output_file: Path, content: str) -> None:
        """Create a plain text file.

        Args:
            output_file: Path where the text file will be saved
            content: Content to write
        """
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)

    def _text_to_html(self, text: str) -> str:
        """Convert plain text to HTML.

        Args:
            text: Plain text content

        Returns:
            HTML formatted content
        """
        # Split into paragraphs
        paragraphs = text.split("\n\n")

        # Wrap each paragraph in <p> tags
        html_paragraphs = [f"<p>{p.strip()}</p>" for p in paragraphs if p.strip()]

        # Combine into full HTML
        html_content = f"""
        <html>
        <head>
            <title>Content</title>
        </head>
        <body>
            {''.join(html_paragraphs)}
        </body>
        </html>
        """

        return html_content

# Made with Bob
