"""Translation functionality for ebooks."""

from enum import Enum
from pathlib import Path
from typing import Optional

from googletrans import Translator as GoogleTranslator
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

from mkebook.utils.helpers import chunk_text

console = Console()


class TranslationEngine(Enum):
    """Supported translation engines."""

    GOOGLE = "google"
    DEEPL = "deepl"
    OPENAI = "openai"


class Translator:
    """Translate ebook content between languages."""

    def __init__(self, engine: TranslationEngine = TranslationEngine.GOOGLE) -> None:
        """Initialize the translator.

        Args:
            engine: Translation engine to use
        """
        self.engine = engine
        self._validate_engine()

    def _validate_engine(self) -> None:
        """Validate that the selected engine is available.

        Raises:
            ValueError: If the engine is not supported
        """
        if self.engine not in TranslationEngine:
            raise ValueError(f"Unsupported translation engine: {self.engine}")

    def translate(
        self,
        input_file: Path,
        output_file: Path,
        source_lang: str = "auto",
        target_lang: str = "en",
        preserve_format: bool = True,
    ) -> None:
        """Translate an ebook from one language to another.

        Args:
            input_file: Path to the ebook to translate
            output_file: Path where the translated ebook will be saved
            source_lang: Source language code (auto-detect if 'auto')
            target_lang: Target language code
            preserve_format: Whether to preserve original formatting

        Raises:
            FileNotFoundError: If the input file doesn't exist
            ValueError: If language codes are invalid
        """
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")

        if source_lang == target_lang and source_lang != "auto":
            raise ValueError("Source and target languages cannot be the same")

        # Read input content
        content = self._read_ebook(input_file)

        # Translate content
        translated_content = self._translate_text(
            content,
            source_lang=source_lang,
            target_lang=target_lang,
        )

        # Write translated content
        self._write_ebook(
            output_file,
            translated_content,
            preserve_format=preserve_format,
        )

    def _read_ebook(self, file_path: Path) -> str:
        """Read content from an ebook file.

        Args:
            file_path: Path to the ebook file

        Returns:
            Content of the ebook as string
        """
        # TODO: Implement proper ebook parsing based on format
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def _write_ebook(
        self,
        file_path: Path,
        content: str,
        preserve_format: bool = True,
    ) -> None:
        """Write translated content to an ebook file.

        Args:
            file_path: Path where the ebook will be saved
            content: Translated content
            preserve_format: Whether to preserve original formatting
        """
        # TODO: Implement proper ebook writing based on format
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    def _translate_text(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
    ) -> str:
        """Translate text using the selected engine.

        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code

        Returns:
            Translated text
        """
        if self.engine == TranslationEngine.GOOGLE:
            return self._translate_google(text, source_lang, target_lang)
        elif self.engine == TranslationEngine.DEEPL:
            return self._translate_deepl(text, source_lang, target_lang)
        elif self.engine == TranslationEngine.OPENAI:
            return self._translate_openai(text, source_lang, target_lang)
        else:
            raise ValueError(f"Unsupported engine: {self.engine}")

    def _translate_google(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
    ) -> str:
        """Translate text using Google Translate.

        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code

        Returns:
            Translated text
        """
        translator = GoogleTranslator()
        
        # Split text into chunks to avoid API limits
        chunks = chunk_text(text, max_chunk_size=4500)
        translated_chunks = []
        
        console.print(f"[blue]Translating {len(chunks)} text chunks...[/blue]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Translating...", total=len(chunks))
            
            for i, chunk in enumerate(chunks, 1):
                try:
                    # Translate chunk
                    src = source_lang if source_lang != "auto" else "auto"
                    result = translator.translate(
                        chunk,
                        src=src,
                        dest=target_lang
                    )
                    translated_chunks.append(result.text)
                    progress.update(task, advance=1)
                    
                except Exception as e:
                    console.print(f"[yellow]Warning: Failed to translate chunk {i}: {e}[/yellow]")
                    # Keep original text if translation fails
                    translated_chunks.append(chunk)
        
        return "\n\n".join(translated_chunks)

    def _translate_deepl(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
    ) -> str:
        """Translate text using DeepL.

        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code

        Returns:
            Translated text

        Note:
            This is a placeholder. Actual implementation requires
            the deepl library and API key.
        """
        # TODO: Implement DeepL integration
        raise NotImplementedError("DeepL integration is not yet implemented")

    def _translate_openai(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
    ) -> str:
        """Translate text using OpenAI.

        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code

        Returns:
            Translated text

        Note:
            This is a placeholder. Actual implementation requires
            the openai library and API key.
        """
        # TODO: Implement OpenAI integration
        raise NotImplementedError("OpenAI integration is not yet implemented")

    def get_supported_languages(self) -> list[str]:
        """Get list of supported language codes for the current engine.

        Returns:
            List of supported language codes
        """
        # Common language codes
        common_languages = [
            "en",  # English
            "es",  # Spanish
            "fr",  # French
            "de",  # German
            "it",  # Italian
            "pt",  # Portuguese
            "ru",  # Russian
            "ja",  # Japanese
            "ko",  # Korean
            "zh",  # Chinese
            "ar",  # Arabic
            "hi",  # Hindi
        ]

        # TODO: Return engine-specific supported languages
        return common_languages

# Made with Bob
