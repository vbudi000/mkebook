# mkebook Examples

This directory contains example scripts and configuration files for using mkebook.

## Files

### `basic_usage.py`
Demonstrates basic usage of the mkebook Python API:
- Creating EPUB ebooks
- Creating plain text ebooks
- Translation setup (placeholder)
- Batch processing multiple files

**Run it:**
```bash
python examples/basic_usage.py
```

### `mkebook.yaml`
Example configuration file showing all available options:
- Default settings for ebook creation
- Translation engine configuration
- Output preferences
- API key setup
- Performance tuning

**Use it:**
```bash
# Copy to your project directory
cp examples/mkebook.yaml .

# Edit with your preferences
nano mkebook.yaml

# mkebook will automatically use it
mkebook create input.txt output.epub
```

## Quick Examples

### Create an EPUB

```bash
mkebook create story.txt story.epub \
  --title "My Story" \
  --author "John Doe" \
  --language en
```

### Translate an Ebook

```bash
mkebook translate book.epub book_es.epub \
  --source-lang en \
  --target-lang es \
  --engine google
```

### Create and Translate

```bash
mkebook convert-and-translate input.txt output_fr.epub \
  --target-lang fr \
  --format epub
```

## Python API Examples

### Simple Ebook Creation

```python
from pathlib import Path
from mkebook import EbookCreator, EbookFormat

creator = EbookCreator()
creator.create(
    input_file=Path("input.txt"),
    output_file=Path("output.epub"),
    format=EbookFormat.EPUB,
    title="My Book",
    author="Jane Doe"
)
```

### Translation

```python
from pathlib import Path
from mkebook import Translator, TranslationEngine

translator = Translator(engine=TranslationEngine.GOOGLE)
translator.translate(
    input_file=Path("book.epub"),
    output_file=Path("book_es.epub"),
    source_lang="en",
    target_lang="es"
)
```

### Batch Processing

```python
from pathlib import Path
from mkebook import EbookCreator, EbookFormat

creator = EbookCreator()
input_dir = Path("input_texts")
output_dir = Path("output_ebooks")
output_dir.mkdir(exist_ok=True)

for txt_file in input_dir.glob("*.txt"):
    output_file = output_dir / f"{txt_file.stem}.epub"
    creator.create(
        input_file=txt_file,
        output_file=output_file,
        format=EbookFormat.EPUB,
        title=txt_file.stem.replace("_", " ").title()
    )
    print(f"Created: {output_file}")
```

## Advanced Examples

### Custom Error Handling

```python
from pathlib import Path
from mkebook import EbookCreator, EbookFormat

def safe_create_ebook(input_path: str, output_path: str) -> bool:
    """Create ebook with error handling."""
    try:
        creator = EbookCreator()
        creator.create(
            input_file=Path(input_path),
            output_file=Path(output_path),
            format=EbookFormat.EPUB
        )
        print(f"✓ Success: {output_path}")
        return True
    except FileNotFoundError:
        print(f"✗ Error: Input file not found: {input_path}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

# Usage
safe_create_ebook("input.txt", "output.epub")
```

### Progress Tracking

```python
from pathlib import Path
from mkebook import EbookCreator, EbookFormat
from rich.progress import Progress, SpinnerColumn, TextColumn

def create_with_progress(files: list[Path]) -> None:
    """Create multiple ebooks with progress tracking."""
    creator = EbookCreator()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task("Creating ebooks...", total=len(files))
        
        for input_file in files:
            output_file = input_file.with_suffix(".epub")
            creator.create(
                input_file=input_file,
                output_file=output_file,
                format=EbookFormat.EPUB
            )
            progress.advance(task)

# Usage
files = list(Path("input").glob("*.txt"))
create_with_progress(files)
```

## Tips

1. **Use Type Hints**: Enable better IDE support and catch errors early
2. **Handle Errors**: Always wrap file operations in try-except blocks
3. **Validate Input**: Check file existence before processing
4. **Use Pathlib**: Prefer `Path` objects over string paths
5. **Test First**: Test with small files before processing large batches

## More Resources

- [Usage Guide](../docs/usage.md) - Comprehensive usage documentation
- [API Reference](../docs/api.md) - Complete API documentation
- [Contributing](../CONTRIBUTING.md) - How to contribute examples

## Need Help?

- Open an [issue](https://github.com/yourusername/mkebook/issues) for bugs
- Start a [discussion](https://github.com/yourusername/mkebook/discussions) for questions
- Check the [documentation](../docs/) for detailed guides