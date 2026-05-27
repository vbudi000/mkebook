# mkebook Documentation

Welcome to the mkebook documentation! This tool helps you create and translate ebooks in various formats.

## Overview

mkebook is a Python package that provides:

- **Ebook Creation**: Convert text files into ebooks (EPUB, PDF, MOBI, TXT)
- **Translation**: Translate ebooks between different languages
- **Combined Workflow**: Create and translate in one step

## Features

✨ **Multiple Formats**: Support for EPUB, PDF, MOBI, and plain text
🌍 **Translation**: Translate ebooks using Google Translate, DeepL, or OpenAI
🎨 **Format Preservation**: Maintain original formatting during translation
⚡ **Fast Processing**: Efficient handling of large documents
🔧 **CLI Interface**: Easy-to-use command-line interface
📦 **Python API**: Programmatic access for integration

## Quick Start

### Installation

```bash
# Using uv (recommended)
uv pip install mkebook

# Using pip
pip install mkebook
```

### Basic Usage

Create an ebook:
```bash
mkebook create input.txt output.epub --title "My Book" --author "John Doe"
```

Translate an ebook:
```bash
mkebook translate input.epub output.epub --target-lang es
```

Create and translate in one step:
```bash
mkebook convert-and-translate input.txt output.epub --target-lang fr
```

## Documentation Sections

- [Usage Guide](usage.md) - Detailed usage instructions and examples
- [API Reference](api.md) - Python API documentation
- [Contributing](../CONTRIBUTING.md) - How to contribute to the project

## Requirements

- Python 3.11 or higher
- Dependencies are automatically installed with the package

## License

mkebook is licensed under the GNU General Public License v3.0 or later (GPL-3.0-or-later).

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/mkebook/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/mkebook/discussions)

## Acknowledgments

mkebook uses the following excellent libraries:

- [ebooklib](https://github.com/aerkalov/ebooklib) - EPUB reading and writing
- [Click](https://click.palletsprojects.com/) - Command-line interface
- [Rich](https://rich.readthedocs.io/) - Beautiful terminal output
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML/XML parsing