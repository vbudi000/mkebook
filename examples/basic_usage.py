#!/usr/bin/env python3
"""Basic usage examples for mkebook.

This script demonstrates how to use mkebook programmatically.
"""

from pathlib import Path

from mkebook import EbookCreator, EbookFormat, Translator, TranslationEngine


def example_create_ebook() -> None:
    """Example: Create an EPUB ebook from a text file."""
    print("Example 1: Creating an EPUB ebook")
    print("-" * 50)

    # Create sample input file
    input_file = Path("sample_input.txt")
    input_file.write_text(
        """Chapter 1: The Beginning

This is the first chapter of our story.
It introduces the main characters and setting.

Chapter 2: The Journey

The adventure begins as our heroes set out on their quest.
They face many challenges along the way.

Chapter 3: The End

Finally, they reach their destination and achieve their goal.
The story concludes with a satisfying resolution.""",
        encoding="utf-8",
    )

    # Create ebook
    creator = EbookCreator()
    output_file = Path("my_book.epub")

    creator.create(
        input_file=input_file,
        output_file=output_file,
        format=EbookFormat.EPUB,
        title="My First Book",
        author="John Doe",
        language="en",
    )

    print(f"✓ Created ebook: {output_file}")
    print(f"  Input: {input_file}")
    print(f"  Format: EPUB")
    print()

    # Cleanup
    input_file.unlink()


def example_translate_ebook() -> None:
    """Example: Translate an ebook (placeholder)."""
    print("Example 2: Translating an ebook")
    print("-" * 50)

    # Note: This is a placeholder example
    # Actual translation requires API keys and implementation

    translator = Translator(engine=TranslationEngine.GOOGLE)

    print(f"✓ Translator initialized with engine: {translator.engine.value}")
    print("  Supported languages:", translator.get_supported_languages()[:5], "...")
    print("  Note: Translation features are under development")
    print()


def example_create_txt_ebook() -> None:
    """Example: Create a plain text ebook."""
    print("Example 3: Creating a plain text ebook")
    print("-" * 50)

    # Create sample input
    input_file = Path("sample_markdown.md")
    input_file.write_text(
        """# My Document

## Introduction

This is a sample document in Markdown format.

## Content

- Point 1
- Point 2
- Point 3

## Conclusion

Thank you for reading!""",
        encoding="utf-8",
    )

    # Create text ebook
    creator = EbookCreator()
    output_file = Path("my_document.txt")

    creator.create(
        input_file=input_file,
        output_file=output_file,
        format=EbookFormat.TXT,
        title="My Document",
    )

    print(f"✓ Created text file: {output_file}")
    print(f"  Input: {input_file}")
    print(f"  Format: TXT")
    print()

    # Cleanup
    input_file.unlink()


def example_batch_processing() -> None:
    """Example: Batch process multiple files."""
    print("Example 4: Batch processing")
    print("-" * 50)

    # Create sample files
    input_dir = Path("input_files")
    input_dir.mkdir(exist_ok=True)

    for i in range(1, 4):
        file_path = input_dir / f"story_{i}.txt"
        file_path.write_text(
            f"Story {i}\n\nThis is the content of story number {i}.",
            encoding="utf-8",
        )

    # Process all files
    output_dir = Path("output_ebooks")
    output_dir.mkdir(exist_ok=True)

    creator = EbookCreator()
    processed = 0

    for txt_file in input_dir.glob("*.txt"):
        output_file = output_dir / f"{txt_file.stem}.epub"

        creator.create(
            input_file=txt_file,
            output_file=output_file,
            format=EbookFormat.EPUB,
            title=txt_file.stem.replace("_", " ").title(),
        )

        processed += 1
        print(f"  ✓ Processed: {txt_file.name} -> {output_file.name}")

    print(f"\n✓ Batch processing complete: {processed} files")
    print()

    # Cleanup
    import shutil

    shutil.rmtree(input_dir)
    shutil.rmtree(output_dir)


def main() -> None:
    """Run all examples."""
    print("=" * 50)
    print("mkebook - Basic Usage Examples")
    print("=" * 50)
    print()

    try:
        example_create_ebook()
        example_translate_ebook()
        example_create_txt_ebook()
        example_batch_processing()

        print("=" * 50)
        print("All examples completed successfully!")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()

# Made with Bob
