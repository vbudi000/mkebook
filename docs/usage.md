# Usage Guide

This guide covers all the features and commands available in mkebook.

## Installation

### Using uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows

# Install mkebook
uv pip install mkebook
```

### Using pip

```bash
pip install mkebook
```

### Development Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/mkebook.git
cd mkebook

# Install with development dependencies
uv pip install -e ".[dev]"
```

## Command-Line Interface

### Creating Ebooks

The `create` command converts text files into ebooks.

#### Basic Usage

```bash
mkebook create input.txt output.epub
```

#### With Options

```bash
mkebook create input.txt output.epub \
  --format epub \
  --title "My Amazing Book" \
  --author "Jane Doe" \
  --language en
```

#### Supported Formats

- **EPUB** (`.epub`) - Default, widely supported
- **PDF** (`.pdf`) - Coming soon
- **MOBI** (`.mobi`) - Coming soon
- **TXT** (`.txt`) - Plain text

#### Examples

Create an EPUB with metadata:
```bash
mkebook create story.txt story.epub \
  --title "The Great Adventure" \
  --author "John Smith" \
  --language en
```

Create a plain text file:
```bash
mkebook create input.md output.txt --format txt
```

### Translating Ebooks

The `translate` command translates ebooks between languages.

#### Basic Usage

```bash
mkebook translate input.epub output.epub --target-lang es
```

#### With Options

```bash
mkebook translate input.epub output.epub \
  --source-lang en \
  --target-lang es \
  --engine google \
  --preserve-format
```

#### Translation Engines

- **google** - Google Translate (default)
- **deepl** - DeepL (requires API key)
- **openai** - OpenAI GPT (requires API key)

#### Language Codes

Common language codes:
- `en` - English
- `es` - Spanish
- `fr` - French
- `de` - German
- `it` - Italian
- `pt` - Portuguese
- `ru` - Russian
- `ja` - Japanese
- `ko` - Korean
- `zh` - Chinese
- `ar` - Arabic

Use `auto` for automatic source language detection.

#### Examples

Translate from English to Spanish:
```bash
mkebook translate book.epub book_es.epub \
  --source-lang en \
  --target-lang es
```

Auto-detect source language:
```bash
mkebook translate book.epub book_fr.epub \
  --source-lang auto \
  --target-lang fr
```

Use DeepL for translation:
```bash
mkebook translate book.epub book_de.epub \
  --target-lang de \
  --engine deepl
```

### Combined Workflow

The `convert-and-translate` command creates and translates in one step.

#### Basic Usage

```bash
mkebook convert-and-translate input.txt output.epub --target-lang es
```

#### With Options

```bash
mkebook convert-and-translate input.txt output.epub \
  --target-lang fr \
  --format epub \
  --engine google
```

#### Examples

Create and translate to Spanish:
```bash
mkebook convert-and-translate story.txt story_es.epub \
  --target-lang es \
  --format epub
```

Create and translate to multiple languages:
```bash
# Spanish
mkebook convert-and-translate book.txt book_es.epub --target-lang es

# French
mkebook convert-and-translate book.txt book_fr.epub --target-lang fr

# German
mkebook convert-and-translate book.txt book_de.epub --target-lang de
```

## Python API

You can also use mkebook programmatically in your Python code.

### Creating Ebooks

```python
from pathlib import Path
from mkebook import EbookCreator, EbookFormat

# Create an ebook creator
creator = EbookCreator()

# Create an EPUB
creator.create(
    input_file=Path("input.txt"),
    output_file=Path("output.epub"),
    format=EbookFormat.EPUB,
    title="My Book",
    author="John Doe",
    language="en"
)
```

### Translating Ebooks

```python
from pathlib import Path
from mkebook import Translator, TranslationEngine

# Create a translator
translator = Translator(engine=TranslationEngine.GOOGLE)

# Translate an ebook
translator.translate(
    input_file=Path("book.epub"),
    output_file=Path("book_es.epub"),
    source_lang="en",
    target_lang="es",
    preserve_format=True
)
```

### Combined Workflow

```python
from pathlib import Path
from mkebook import EbookCreator, Translator, EbookFormat, TranslationEngine

# Step 1: Create ebook
creator = EbookCreator()
temp_file = Path("temp.epub")

creator.create(
    input_file=Path("input.txt"),
    output_file=temp_file,
    format=EbookFormat.EPUB,
    title="My Book"
)

# Step 2: Translate
translator = Translator(engine=TranslationEngine.GOOGLE)

translator.translate(
    input_file=temp_file,
    output_file=Path("output_es.epub"),
    source_lang="auto",
    target_lang="es"
)

# Cleanup
temp_file.unlink()
```

## Configuration

### Environment Variables

Set API keys for translation services:

```bash
# DeepL
export DEEPL_API_KEY="your-api-key"

# OpenAI
export OPENAI_API_KEY="your-api-key"
```

### Configuration File

Create a `mkebook.yaml` file in your project directory:

```yaml
# Default settings
default_format: epub
default_language: en
preserve_format: true

# Translation settings
translation:
  engine: google
  chunk_size: 5000

# Ebook settings
ebook:
  default_author: "Your Name"
```

## Tips and Best Practices

### For Best Results

1. **Use clean input**: Remove unnecessary formatting from source files
2. **Choose the right format**: EPUB for most ebook readers, TXT for simplicity
3. **Chunk large files**: Break very large books into chapters for better translation
4. **Review translations**: Always review machine translations for accuracy
5. **Preserve formatting**: Use `--preserve-format` to maintain structure

### Performance

- Translation speed depends on the chosen engine and text length
- Large files are automatically chunked for efficient processing
- Use local caching to avoid re-translating the same content

### Troubleshooting

**Issue**: Translation fails with API error
- **Solution**: Check your API key and internet connection

**Issue**: Output format not supported
- **Solution**: Currently only EPUB and TXT are fully supported

**Issue**: Formatting lost during translation
- **Solution**: Use `--preserve-format` flag

## Next Steps

- Check the [API Reference](api.md) for detailed function documentation
- See [Contributing Guide](../CONTRIBUTING.md) to help improve mkebook
- Report issues on [GitHub](https://github.com/yourusername/mkebook/issues)