# API Reference

This document provides detailed information about the mkebook Python API.

## Core Modules

### mkebook.core.ebook

#### EbookFormat

Enumeration of supported ebook formats.

```python
from mkebook import EbookFormat

class EbookFormat(Enum):
    EPUB = "epub"
    PDF = "pdf"
    MOBI = "mobi"
    TXT = "txt"
```

**Values:**
- `EPUB`: EPUB format (widely supported)
- `PDF`: PDF format (coming soon)
- `MOBI`: MOBI format for Kindle (coming soon)
- `TXT`: Plain text format

#### EbookCreator

Class for creating ebooks from various input formats.

```python
from mkebook import EbookCreator, EbookFormat
from pathlib import Path

creator = EbookCreator()
```

**Methods:**

##### `create()`

Create an ebook from an input file.

```python
def create(
    self,
    input_file: Path,
    output_file: Path,
    format: EbookFormat = EbookFormat.EPUB,
    title: Optional[str] = None,
    author: Optional[str] = None,
    language: str = "en",
) -> None
```

**Parameters:**
- `input_file` (Path): Path to the source file
- `output_file` (Path): Path where the ebook will be saved
- `format` (EbookFormat): Output format (default: EPUB)
- `title` (str, optional): Title of the ebook (defaults to filename)
- `author` (str, optional): Author of the ebook
- `language` (str): Language code (default: "en")

**Raises:**
- `FileNotFoundError`: If the input file doesn't exist
- `ValueError`: If the format is not supported
- `NotImplementedError`: For PDF and MOBI formats (coming soon)

**Example:**

```python
from pathlib import Path
from mkebook import EbookCreator, EbookFormat

creator = EbookCreator()
creator.create(
    input_file=Path("story.txt"),
    output_file=Path("story.epub"),
    format=EbookFormat.EPUB,
    title="My Story",
    author="John Doe",
    language="en"
)
```

### mkebook.core.translator

#### TranslationEngine

Enumeration of supported translation engines.

```python
from mkebook import TranslationEngine

class TranslationEngine(Enum):
    GOOGLE = "google"
    DEEPL = "deepl"
    OPENAI = "openai"
```

**Values:**
- `GOOGLE`: Google Translate
- `DEEPL`: DeepL Translator
- `OPENAI`: OpenAI GPT-based translation

#### Translator

Class for translating ebook content between languages.

```python
from mkebook import Translator, TranslationEngine

translator = Translator(engine=TranslationEngine.GOOGLE)
```

**Constructor Parameters:**
- `engine` (TranslationEngine): Translation engine to use (default: GOOGLE)

**Methods:**

##### `translate()`

Translate an ebook from one language to another.

```python
def translate(
    self,
    input_file: Path,
    output_file: Path,
    source_lang: str = "auto",
    target_lang: str = "en",
    preserve_format: bool = True,
) -> None
```

**Parameters:**
- `input_file` (Path): Path to the ebook to translate
- `output_file` (Path): Path where the translated ebook will be saved
- `source_lang` (str): Source language code (default: "auto" for auto-detection)
- `target_lang` (str): Target language code (default: "en")
- `preserve_format` (bool): Whether to preserve original formatting (default: True)

**Raises:**
- `FileNotFoundError`: If the input file doesn't exist
- `ValueError`: If language codes are invalid or the same
- `NotImplementedError`: Translation engines not yet fully implemented

**Example:**

```python
from pathlib import Path
from mkebook import Translator, TranslationEngine

translator = Translator(engine=TranslationEngine.GOOGLE)
translator.translate(
    input_file=Path("book.epub"),
    output_file=Path("book_es.epub"),
    source_lang="en",
    target_lang="es",
    preserve_format=True
)
```

##### `get_supported_languages()`

Get list of supported language codes for the current engine.

```python
def get_supported_languages(self) -> list[str]
```

**Returns:**
- `list[str]`: List of supported language codes

**Example:**

```python
translator = Translator()
languages = translator.get_supported_languages()
print(languages)  # ['en', 'es', 'fr', 'de', ...]
```

## Utility Modules

### mkebook.utils.helpers

Utility functions for common tasks.

#### `format_file_size()`

Format file size in bytes to human-readable format.

```python
def format_file_size(size_bytes: int) -> str
```

**Parameters:**
- `size_bytes` (int): Size in bytes

**Returns:**
- `str`: Formatted string (e.g., "1.5 MB", "500 KB")

**Example:**

```python
from mkebook.utils import format_file_size

size = format_file_size(1536000)
print(size)  # "1.5 MB"
```

#### `validate_language_code()`

Validate if a language code is in the correct format.

```python
def validate_language_code(code: str) -> bool
```

**Parameters:**
- `code` (str): Language code to validate (e.g., 'en', 'es', 'zh-CN')

**Returns:**
- `bool`: True if valid, False otherwise

**Example:**

```python
from mkebook.utils import validate_language_code

is_valid = validate_language_code("en")  # True
is_valid = validate_language_code("eng")  # False
```

#### `sanitize_filename()`

Sanitize a filename by removing invalid characters.

```python
def sanitize_filename(filename: str) -> str
```

**Parameters:**
- `filename` (str): Original filename

**Returns:**
- `str`: Sanitized filename safe for filesystem

**Example:**

```python
from mkebook.utils import sanitize_filename

safe_name = sanitize_filename("my<file>name.txt")
print(safe_name)  # "my_file_name.txt"
```

#### `chunk_text()`

Split text into chunks for translation.

```python
def chunk_text(text: str, max_chunk_size: int = 5000) -> list[str]
```

**Parameters:**
- `text` (str): Text to split
- `max_chunk_size` (int): Maximum size of each chunk in characters (default: 5000)

**Returns:**
- `list[str]`: List of text chunks

**Example:**

```python
from mkebook.utils import chunk_text

long_text = "..." * 10000
chunks = chunk_text(long_text, max_chunk_size=5000)
print(f"Split into {len(chunks)} chunks")
```

## Type Hints

mkebook uses type hints throughout the codebase for better IDE support and type checking.

```python
from pathlib import Path
from typing import Optional
from mkebook import EbookCreator, EbookFormat

def create_my_ebook(
    input_path: Path,
    output_path: Path,
    title: Optional[str] = None
) -> None:
    creator = EbookCreator()
    creator.create(
        input_file=input_path,
        output_file=output_path,
        format=EbookFormat.EPUB,
        title=title
    )
```

## Error Handling

All functions raise appropriate exceptions for error conditions:

```python
from pathlib import Path
from mkebook import EbookCreator

creator = EbookCreator()

try:
    creator.create(
        input_file=Path("nonexistent.txt"),
        output_file=Path("output.epub")
    )
except FileNotFoundError as e:
    print(f"Input file not found: {e}")
except ValueError as e:
    print(f"Invalid parameter: {e}")
except NotImplementedError as e:
    print(f"Feature not yet implemented: {e}")
```

## Advanced Usage

### Custom Translation Pipeline

```python
from pathlib import Path
from mkebook import Translator, TranslationEngine
from mkebook.utils import chunk_text

# Read content
with open("large_book.txt", "r") as f:
    content = f.read()

# Split into manageable chunks
chunks = chunk_text(content, max_chunk_size=3000)

# Translate each chunk
translator = Translator(engine=TranslationEngine.GOOGLE)
translated_chunks = []

for i, chunk in enumerate(chunks):
    print(f"Translating chunk {i+1}/{len(chunks)}...")
    # Note: This is a simplified example
    # Actual implementation would use the translator's internal methods
    translated_chunks.append(chunk)  # Placeholder

# Combine translated chunks
translated_content = "\n\n".join(translated_chunks)

# Save result
with open("translated_book.txt", "w") as f:
    f.write(translated_content)
```

### Batch Processing

```python
from pathlib import Path
from mkebook import EbookCreator, EbookFormat

def batch_convert(input_dir: Path, output_dir: Path) -> None:
    """Convert all text files in a directory to EPUB."""
    creator = EbookCreator()
    output_dir.mkdir(exist_ok=True)
    
    for txt_file in input_dir.glob("*.txt"):
        output_file = output_dir / f"{txt_file.stem}.epub"
        print(f"Converting {txt_file.name}...")
        
        creator.create(
            input_file=txt_file,
            output_file=output_file,
            format=EbookFormat.EPUB,
            title=txt_file.stem
        )

# Usage
batch_convert(Path("input_texts"), Path("output_ebooks"))
```

## See Also

- [Usage Guide](usage.md) - Practical examples and CLI usage
- [Contributing](../CONTRIBUTING.md) - How to contribute to mkebook
- [GitHub Repository](https://github.com/yourusername/mkebook)