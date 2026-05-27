"""Core functionality for mkebook."""

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
]

# Made with Bob
