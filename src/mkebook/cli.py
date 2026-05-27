"""Command-line interface for mkebook."""

from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from mkebook import __version__
from mkebook.core.ebook import EbookCreator, EbookFormat
from mkebook.core.translator import Translator, TranslationEngine
from mkebook.core.scraper import NovelScraper

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="mkebook")
@click.pass_context
def main(ctx: click.Context) -> None:
    """mkebook - Make ebook and translate it.

    A tool for creating and translating ebooks in various formats.
    """
    ctx.ensure_object(dict)


@main.command()
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.argument("output_file", type=click.Path(path_type=Path))
@click.option(
    "--format",
    "-f",
    type=click.Choice(["epub", "pdf", "mobi", "txt"], case_sensitive=False),
    default="epub",
    help="Output format for the ebook.",
)
@click.option(
    "--title",
    "-t",
    help="Title of the ebook.",
)
@click.option(
    "--author",
    "-a",
    help="Author of the ebook.",
)
@click.option(
    "--language",
    "-l",
    default="en",
    help="Language code (e.g., en, es, fr).",
)
def create(
    input_file: Path,
    output_file: Path,
    format: str,
    title: Optional[str],
    author: Optional[str],
    language: str,
) -> None:
    """Create an ebook from input file.

    INPUT_FILE: Path to the source file (text, markdown, etc.)
    OUTPUT_FILE: Path where the ebook will be saved
    """
    try:
        console.print(f"[bold blue]Creating ebook from {input_file}...[/bold blue]")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Processing...", total=None)

            creator = EbookCreator()
            ebook_format = EbookFormat[format.upper()]

            creator.create(
                input_file=input_file,
                output_file=output_file,
                format=ebook_format,
                title=title,
                author=author,
                language=language,
            )

            progress.update(task, completed=True)

        console.print(f"[bold green]✓[/bold green] Ebook created: {output_file}")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise click.Abort()


@main.command()
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.argument("output_file", type=click.Path(path_type=Path))
@click.option(
    "--source-lang",
    "-s",
    default="auto",
    help="Source language code (auto-detect if not specified).",
)
@click.option(
    "--target-lang",
    "-t",
    required=True,
    help="Target language code for translation.",
)
@click.option(
    "--engine",
    "-e",
    type=click.Choice(["google", "deepl", "openai"], case_sensitive=False),
    default="google",
    help="Translation engine to use.",
)
@click.option(
    "--preserve-format",
    is_flag=True,
    default=True,
    help="Preserve original formatting.",
)
def translate(
    input_file: Path,
    output_file: Path,
    source_lang: str,
    target_lang: str,
    engine: str,
    preserve_format: bool,
) -> None:
    """Translate an ebook to another language.

    INPUT_FILE: Path to the ebook to translate
    OUTPUT_FILE: Path where the translated ebook will be saved
    """
    try:
        console.print(
            f"[bold blue]Translating {input_file} from {source_lang} to {target_lang}...[/bold blue]"
        )

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Translating...", total=None)

            translator = Translator(engine=TranslationEngine[engine.upper()])

            translator.translate(
                input_file=input_file,
                output_file=output_file,
                source_lang=source_lang,
                target_lang=target_lang,
                preserve_format=preserve_format,
            )

            progress.update(task, completed=True)

        console.print(f"[bold green]✓[/bold green] Translation complete: {output_file}")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise click.Abort()


@main.command()
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.argument("output_file", type=click.Path(path_type=Path))
@click.option(
    "--target-lang",
    "-t",
    required=True,
    help="Target language code for translation.",
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["epub", "pdf", "mobi", "txt"], case_sensitive=False),
    default="epub",
    help="Output format for the ebook.",
)
@click.option(
    "--engine",
    "-e",
    type=click.Choice(["google", "deepl", "openai"], case_sensitive=False),
    default="google",
    help="Translation engine to use.",
)
def convert_and_translate(
    input_file: Path,
    output_file: Path,
    target_lang: str,
    format: str,
    engine: str,
) -> None:
    """Create and translate an ebook in one step.

    INPUT_FILE: Path to the source file
    OUTPUT_FILE: Path where the translated ebook will be saved
    """
    try:
        console.print(
            f"[bold blue]Creating and translating ebook to {target_lang}...[/bold blue]"
        )

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Step 1: Create ebook
            task1 = progress.add_task("Creating ebook...", total=None)
            creator = EbookCreator()
            temp_file = output_file.with_suffix(".temp" + output_file.suffix)

            creator.create(
                input_file=input_file,
                output_file=temp_file,
                format=EbookFormat[format.upper()],
            )
            progress.update(task1, completed=True)

            # Step 2: Translate
            task2 = progress.add_task("Translating...", total=None)
            translator = Translator(engine=TranslationEngine[engine.upper()])

            translator.translate(
                input_file=temp_file,
                output_file=output_file,
                source_lang="auto",
                target_lang=target_lang,
                preserve_format=True,
            )
            progress.update(task2, completed=True)

            # Cleanup
            temp_file.unlink(missing_ok=True)

        console.print(
            f"[bold green]✓[/bold green] Ebook created and translated: {output_file}"
        )

    except Exception as e:

@main.command()
@click.argument("url", type=str)
@click.argument("output_file", type=click.Path(path_type=Path))
@click.option(
    "--title",
    "-t",
    help="Title of the ebook (auto-detected if not provided).",
)
@click.option(
    "--author",
    "-a",
    help="Author of the ebook.",
)
@click.option(
    "--translate",
    is_flag=True,
    default=False,
    help="Translate the ebook after scraping.",
)
@click.option(
    "--source-lang",
    "-s",
    default="zh-cn",
    help="Source language code (default: zh-cn for Chinese Simplified).",
)
@click.option(
    "--target-lang",
    "-l",
    default="en",
    help="Target language code (default: en for English).",
)
@click.option(
    "--start-chapter",
    type=int,
    default=1,
    help="Starting chapter number (1-indexed).",
)
@click.option(
    "--end-chapter",
    type=int,
    help="Ending chapter number (inclusive).",
)
@click.option(
    "--max-chapters",
    type=int,
    help="Maximum number of chapters to scrape.",
)
@click.option(
    "--delay",
    type=float,
    default=1.0,
    help="Delay between requests in seconds (default: 1.0).",
)
def scrape(
    url: str,
    output_file: Path,
    title: Optional[str],
    author: Optional[str],
    translate: bool,
    source_lang: str,
    target_lang: str,
    start_chapter: int,
    end_chapter: Optional[int],
    max_chapters: Optional[int],
    delay: float,
) -> None:
    """Scrape a web novel and create an ebook.

    URL: URL of the table of contents page
    OUTPUT_FILE: Path where the ebook will be saved
    
    Example:
        mkebook scrape https://www.69shuba.com/book/35785/ output.epub --translate
    """
    try:
        console.print(f"[bold blue]Scraping novel from {url}...[/bold blue]")

        # Initialize scraper
        scraper = NovelScraper(delay=delay)

        # Scrape chapters
        chapters = scraper.scrape_novel(
            toc_url=url,
            start_chapter=start_chapter,
            end_chapter=end_chapter,
            max_chapters=max_chapters,
        )

        if not chapters:
            console.print("[bold red]Error:[/bold red] No chapters found")
            raise click.Abort()

        # Use first chapter title as book title if not provided
        if title is None:
            title = "Web Novel"
            # Try to extract book title from URL or page
            console.print(f"[yellow]Using default title: {title}[/yellow]")

        # Prepare chapter data
        if translate:
            console.print(
                f"[bold blue]Translating from {source_lang} to {target_lang}...[/bold blue]"
            )
            translator = Translator(engine=TranslationEngine.GOOGLE)
            
            translated_chapters = []
            for chapter in chapters:
                # Translate title and content
                translated_title = translator._translate_text(
                    chapter.title,
                    source_lang=source_lang,
                    target_lang=target_lang,
                )
                translated_content = translator._translate_text(
                    chapter.content,
                    source_lang=source_lang,
                    target_lang=target_lang,
                )
                translated_chapters.append((translated_title, translated_content))
            
            chapter_data = translated_chapters
        else:
            chapter_data = [(ch.title, ch.content) for ch in chapters]

        # Create ebook
        console.print("[bold blue]Creating ebook...[/bold blue]")
        creator = EbookCreator()
        creator.create_from_chapters(
            chapters=chapter_data,
            output_file=output_file,
            title=title,
            author=author,
            language=target_lang if translate else source_lang,
        )

        console.print(f"[bold green]✓[/bold green] Ebook created successfully: {output_file}")
        console.print(f"[green]Total chapters: {len(chapters)}[/green]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise click.Abort()

        console.print(f"[bold red]Error:[/bold red] {e}")
        raise click.Abort()


if __name__ == "__main__":
    main()

# Made with Bob
