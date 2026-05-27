"""mkebook - Make ebook and translate it.

A Python package for creating and translating ebooks in various formats.
"""

__version__ = "0.1.0"
__author__ = "mkebook contributors"
__license__ = "GPL-3.0-or-later"

from mkebook.core.ebook import EbookCreator, EbookFormat
from mkebook.core.translator import Translator, TranslationEngine
from mkebook.core.scraper import NovelScraper, Chapter

__all__ = [
    "EbookCreator",
    "EbookFormat",
    "Translator",
    "TranslationEngine",
    "NovelScraper",
    "Chapter",
    "__version__",
]

# Made with Bob
