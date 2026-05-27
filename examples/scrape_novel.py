"""Example: Scrape a web novel and create an ebook with translation.

This example demonstrates how to:
1. Scrape chapters from a Chinese web novel website
2. Translate the content from Chinese to English
3. Create an EPUB ebook with the translated content
"""

from pathlib import Path
from mkebook import NovelScraper, EbookCreator, Translator, TranslationEngine

def main():
    # Configuration
    novel_url = "https://www.69shuba.com/book/35785/"  # Table of contents URL
    output_file = Path("translated_novel.epub")
    
    # Step 1: Scrape the novel
    print("Step 1: Scraping novel chapters...")
    scraper = NovelScraper(delay=1.0)  # 1 second delay between requests
    
    # Scrape first 10 chapters as an example
    chapters = scraper.scrape_novel(
        toc_url=novel_url,
        start_chapter=1,
        max_chapters=10,  # Limit to 10 chapters for testing
    )
    
    print(f"Scraped {len(chapters)} chapters")
    
    # Step 2: Translate the chapters
    print("\nStep 2: Translating chapters from Chinese to English...")
    translator = Translator(engine=TranslationEngine.GOOGLE)
    
    translated_chapters = []
    for i, chapter in enumerate(chapters, 1):
        print(f"Translating chapter {i}/{len(chapters)}: {chapter.title}")
        
        # Translate title
        translated_title = translator._translate_text(
            chapter.title,
            source_lang="zh-cn",
            target_lang="en"
        )
        
        # Translate content
        translated_content = translator._translate_text(
            chapter.content,
            source_lang="zh-cn",
            target_lang="en"
        )
        
        translated_chapters.append((translated_title, translated_content))
    
    # Step 3: Create the ebook
    print("\nStep 3: Creating EPUB ebook...")
    creator = EbookCreator()
    creator.create_from_chapters(
        chapters=translated_chapters,
        output_file=output_file,
        title="Translated Web Novel",
        author="Unknown Author",
        language="en",
    )
    
    print(f"\n✓ Success! Ebook created: {output_file}")
    print(f"Total chapters: {len(chapters)}")


if __name__ == "__main__":
    main()

# Made with Bob