# mkebook

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-GPL--3.0-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Make ebook and translate it** - A powerful Python tool for creating and translating ebooks in various formats.

## ✨ Features

- 🌐 **Web Scraping**: Extract chapters from Chinese web novel sites (69shuba.com and more)
- 📚 **Create Ebooks**: Convert text files to EPUB, PDF, MOBI, or TXT formats
- 🌍 **Translate**: Translate ebooks between multiple languages using Google Translate
- 🎨 **Preserve Formatting**: Maintain original structure during translation
- ⚡ **Fast Processing**: Efficient handling of large documents with progress tracking
- 🔧 **CLI & API**: Use via command-line or Python API
- 🎯 **Modern Stack**: Built with Python 3.11+ and uv package manager
- 🧹 **Smart Cleaning**: Automatically removes ads and noise from scraped content

## 🚀 Quick Start

### Installation

Using uv (recommended):
```bash
uv pip install mkebook
```

Using pip:
```bash
pip install mkebook
```

### Basic Usage

**Scrape a web novel and create an ebook with translation:**
```bash
mkebook scrape https://www.69shuba.com/book/35785/ output.epub --translate --max-chapters 10
```

**Scrape without translation:**
```bash
mkebook scrape https://www.69shuba.com/book/35785/ output.epub --max-chapters 10
```

**Create an ebook from a text file:**
```bash
mkebook create input.txt output.epub --title "My Book" --author "John Doe"
```

**Translate an existing ebook:**
```bash
mkebook translate book.epub book_es.epub --target-lang es
```

**Create and translate in one step:**
```bash
mkebook convert-and-translate input.txt output.epub --target-lang fr
```

### Python API Usage

```python
from mkebook import NovelScraper, EbookCreator, Translator, TranslationEngine

# Scrape a web novel
scraper = NovelScraper(delay=1.0)
chapters = scraper.scrape_novel(
    toc_url="https://www.69shuba.com/book/35785/",
    max_chapters=10
)

# Translate chapters
translator = Translator(engine=TranslationEngine.GOOGLE)
translated_chapters = []
for chapter in chapters:
    translated_title = translator._translate_text(
        chapter.title, source_lang="zh-cn", target_lang="en"
    )
    translated_content = translator._translate_text(
        chapter.content, source_lang="zh-cn", target_lang="en"
    )
    translated_chapters.append((translated_title, translated_content))

# Create ebook
creator = EbookCreator()
creator.create_from_chapters(
    chapters=translated_chapters,
    output_file="output.epub",
    title="My Translated Novel",
    language="en"
)
```

## 📖 Documentation

- [Usage Guide](docs/usage.md) - Detailed usage instructions
- [API Reference](docs/api.md) - Python API documentation
- [Examples](examples/) - Code examples and templates

## 🛠️ Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/mkebook.git
cd mkebook

# Create virtual environment with uv
uv venv
source .venv/bin/activate  # On Unix/macOS
# or .venv\Scripts\activate on Windows

# Install with development dependencies
uv pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=mkebook --cov-report=html

# Run specific test file
pytest tests/test_core/test_ebook.py
```

### Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check . --fix

# Type checking
mypy src/
```

## 📋 Requirements

- Python 3.11 or higher
- Dependencies managed via pyproject.toml

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the GNU General Public License v3.0 or later (GPL-3.0-or-later). See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with these excellent libraries:
- [ebooklib](https://github.com/aerkalov/ebooklib) - EPUB reading and writing
- [Click](https://click.palletsprojects.com/) - Command-line interface
- [Rich](https://rich.readthedocs.io/) - Beautiful terminal output
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML/XML parsing

## 📬 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/mkebook/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/mkebook/discussions)

## 🗺️ Roadmap

- [x] Web scraping for Chinese web novels
- [x] Google Translate integration
- [x] Multi-chapter EPUB creation
- [ ] Full PDF generation support
- [ ] MOBI format support
- [ ] Integration with DeepL and OpenAI translation APIs
- [ ] Support for more web novel sites
- [ ] Batch processing improvements
- [ ] GUI interface
- [ ] Plugin system for custom formats

---

Made with ❤️ by the mkebook contributors
