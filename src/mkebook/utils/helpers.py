"""Helper utility functions."""

import re
from pathlib import Path


def format_file_size(size_bytes: int) -> str:
    """Format file size in bytes to human-readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted string (e.g., "1.5 MB", "500 KB")
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def validate_language_code(code: str) -> bool:
    """Validate if a language code is in the correct format.

    Args:
        code: Language code to validate (e.g., 'en', 'es', 'zh-CN')

    Returns:
        True if valid, False otherwise
    """
    # ISO 639-1 (2-letter) or ISO 639-1 with region (e.g., zh-CN)
    pattern = r"^[a-z]{2}(-[A-Z]{2})?$"
    return bool(re.match(pattern, code)) or code == "auto"


def get_file_extension(file_path: Path) -> str:
    """Get the file extension without the dot.

    Args:
        file_path: Path to the file

    Returns:
        File extension in lowercase (e.g., 'epub', 'pdf')
    """
    return file_path.suffix.lstrip(".").lower()


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename by removing invalid characters.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename safe for filesystem
    """
    # Remove invalid characters
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, "_", filename)

    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip(". ")

    # Limit length
    max_length = 255
    if len(sanitized) > max_length:
        name, ext = sanitized.rsplit(".", 1) if "." in sanitized else (sanitized, "")
        name = name[: max_length - len(ext) - 1]
        sanitized = f"{name}.{ext}" if ext else name

    return sanitized or "unnamed"


def chunk_text(text: str, max_chunk_size: int = 5000) -> list[str]:
    """Split text into chunks for translation.

    Args:
        text: Text to split
        max_chunk_size: Maximum size of each chunk in characters

    Returns:
        List of text chunks
    """
    if len(text) <= max_chunk_size:
        return [text]

    chunks = []
    current_chunk = ""

    # Split by paragraphs first
    paragraphs = text.split("\n\n")

    for paragraph in paragraphs:
        # If adding this paragraph exceeds the limit
        if len(current_chunk) + len(paragraph) + 2 > max_chunk_size:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""

            # If a single paragraph is too large, split by sentences
            if len(paragraph) > max_chunk_size:
                sentences = re.split(r"(?<=[.!?])\s+", paragraph)
                for sentence in sentences:
                    if len(current_chunk) + len(sentence) + 1 > max_chunk_size:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = sentence
                    else:
                        current_chunk += " " + sentence if current_chunk else sentence
            else:
                current_chunk = paragraph
        else:
            current_chunk += "\n\n" + paragraph if current_chunk else paragraph

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

# Made with Bob
