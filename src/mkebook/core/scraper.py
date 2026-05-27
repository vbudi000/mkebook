"""Web scraper for extracting chapters from online novels."""

import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

console = Console()


@dataclass
class Chapter:
    """Represents a book chapter."""

    title: str
    content: str
    url: str
    number: int


class NovelScraper:
    """Scrape web novels from various Chinese novel websites."""

    def __init__(
        self,
        delay: float = 1.0,
        timeout: int = 30,
        max_retries: int = 3,
    ) -> None:
        """Initialize the novel scraper.

        Args:
            delay: Delay between requests in seconds
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
        """
        self.delay = delay
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def get_table_of_contents(self, url: str) -> list[tuple[str, str]]:
        """Extract chapter links from table of contents page.

        Args:
            url: URL of the table of contents page

        Returns:
            List of tuples containing (chapter_title, chapter_url)

        Raises:
            ValueError: If unable to extract chapters
        """
        console.print(f"[blue]Fetching table of contents from:[/blue] {url}")
        
        html = self._fetch_page(url)
        soup = BeautifulSoup(html, 'lxml')
        
        # Detect website and use appropriate selectors
        domain = urlparse(url).netloc
        
        if '69shuba.com' in domain or '69shu.com' in domain:
            chapters = self._extract_69shuba_chapters(soup, url)
        else:
            # Generic extraction method
            chapters = self._extract_generic_chapters(soup, url)
        
        if not chapters:
            raise ValueError("No chapters found. The website structure may have changed.")
        
        console.print(f"[green]Found {len(chapters)} chapters[/green]")
        return chapters

    def _extract_69shuba_chapters(
        self,
        soup: BeautifulSoup,
        base_url: str
    ) -> list[tuple[str, str]]:
        """Extract chapters from 69shuba.com website.

        Args:
            soup: BeautifulSoup object of the page
            base_url: Base URL for resolving relative links

        Returns:
            List of tuples containing (chapter_title, chapter_url)
        """
        chapters = []
        
        # Try multiple selectors for chapter links
        selectors = [
            'div.catalog ul li a',
            'div.mulu ul li a',
            'ul.chapter-list li a',
            'div#list dd a',
        ]
        
        for selector in selectors:
            links = soup.select(selector)
            if links:
                for link in links:
                    title = link.get_text(strip=True)
                    href = link.get('href', '')
                    if href and title:
                        full_url = urljoin(base_url, href)
                        chapters.append((title, full_url))
                break
        
        return chapters

    def _extract_generic_chapters(
        self,
        soup: BeautifulSoup,
        base_url: str
    ) -> list[tuple[str, str]]:
        """Generic chapter extraction for unknown websites.

        Args:
            soup: BeautifulSoup object of the page
            base_url: Base URL for resolving relative links

        Returns:
            List of tuples containing (chapter_title, chapter_url)
        """
        chapters = []
        
        # Look for links that might be chapters
        all_links = soup.find_all('a', href=True)
        
        # Filter links that look like chapters
        chapter_pattern = re.compile(r'第.*章|chapter|chap', re.IGNORECASE)
        
        for link in all_links:
            title = link.get_text(strip=True)
            if chapter_pattern.search(title):
                href = link.get('href', '')
                if href:
                    full_url = urljoin(base_url, href)
                    chapters.append((title, full_url))
        
        return chapters

    def scrape_chapter(self, url: str, chapter_num: int) -> Chapter:
        """Scrape a single chapter.

        Args:
            url: URL of the chapter
            chapter_num: Chapter number

        Returns:
            Chapter object with title and content

        Raises:
            ValueError: If unable to extract chapter content
        """
        html = self._fetch_page(url)
        soup = BeautifulSoup(html, 'lxml')
        
        # Extract chapter title
        title = self._extract_chapter_title(soup)
        
        # Extract chapter content
        content = self._extract_chapter_content(soup)
        
        if not content:
            raise ValueError(f"No content found for chapter: {url}")
        
        return Chapter(
            title=title,
            content=content,
            url=url,
            number=chapter_num
        )

    def _extract_chapter_title(self, soup: BeautifulSoup) -> str:
        """Extract chapter title from page.

        Args:
            soup: BeautifulSoup object of the chapter page

        Returns:
            Chapter title
        """
        # Try multiple selectors for title
        selectors = [
            'h1',
            'div.title h1',
            'div.bookname h1',
            'div.content h1',
            'h2',
        ]
        
        for selector in selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                return title_elem.get_text(strip=True)
        
        return "Untitled Chapter"

    def _extract_chapter_content(self, soup: BeautifulSoup) -> str:
        """Extract chapter content from page.

        Args:
            soup: BeautifulSoup object of the chapter page

        Returns:
            Chapter content as plain text
        """
        # Try multiple selectors for content
        selectors = [
            'div#content',
            'div.content',
            'div.txtnav',
            'div#htmlContent',
            'div.read-content',
            'article',
        ]
        
        content_elem = None
        for selector in selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                break
        
        if not content_elem:
            # Fallback: try to find the largest text block
            all_divs = soup.find_all('div')
            content_elem = max(all_divs, key=lambda x: len(x.get_text()), default=None)
        
        if not content_elem:
            return ""
        
        # Clean up the content
        content = self._clean_content(content_elem)
        return content

    def _clean_content(self, element: BeautifulSoup) -> str:
        """Clean and format chapter content.

        Args:
            element: BeautifulSoup element containing the content

        Returns:
            Cleaned content text
        """
        # Remove script and style elements
        for script in element(['script', 'style', 'iframe', 'noscript']):
            script.decompose()
        
        # Get text
        text = element.get_text(separator='\n')
        
        # Clean up common noise
        noise_patterns = [
            r'.*?广告.*?',
            r'.*?推荐.*?',
            r'.*?www\..*?\.com.*?',
            r'.*?http[s]?://.*?',
            r'.*?请记住.*?',
            r'.*?最新章节.*?',
            r'.*?手机用户.*?',
            r'.*?笔趣阁.*?',
            r'.*?69书吧.*?',
            r'.*?69shuba.*?',
        ]
        
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Skip lines matching noise patterns
            skip = False
            for pattern in noise_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    skip = True
                    break
            
            if not skip and len(line) > 5:  # Skip very short lines
                cleaned_lines.append(line)
        
        return '\n\n'.join(cleaned_lines)

    def scrape_novel(
        self,
        toc_url: str,
        start_chapter: int = 1,
        end_chapter: Optional[int] = None,
        max_chapters: Optional[int] = None,
    ) -> list[Chapter]:
        """Scrape multiple chapters from a novel.

        Args:
            toc_url: URL of the table of contents
            start_chapter: Starting chapter number (1-indexed)
            end_chapter: Ending chapter number (inclusive, None for all)
            max_chapters: Maximum number of chapters to scrape

        Returns:
            List of Chapter objects

        Raises:
            ValueError: If unable to scrape chapters
        """
        # Get chapter links
        chapter_links = self.get_table_of_contents(toc_url)
        
        # Determine range
        start_idx = start_chapter - 1
        end_idx = end_chapter if end_chapter else len(chapter_links)
        
        if max_chapters:
            end_idx = min(start_idx + max_chapters, len(chapter_links))
        
        chapter_links = chapter_links[start_idx:end_idx]
        
        console.print(f"[blue]Scraping {len(chapter_links)} chapters...[/blue]")
        
        chapters = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
        ) as progress:
            task = progress.add_task(
                "Scraping chapters...",
                total=len(chapter_links)
            )
            
            for idx, (title, url) in enumerate(chapter_links, start=start_chapter):
                try:
                    chapter = self.scrape_chapter(url, idx)
                    chapters.append(chapter)
                    progress.update(
                        task,
                        advance=1,
                        description=f"Scraped: {chapter.title}"
                    )
                    
                    # Delay between requests
                    if idx < len(chapter_links):
                        time.sleep(self.delay)
                        
                except Exception as e:
                    console.print(f"[red]Error scraping chapter {idx}:[/red] {e}")
                    continue
        
        console.print(f"[green]Successfully scraped {len(chapters)} chapters[/green]")
        return chapters

    def _fetch_page(self, url: str) -> str:
        """Fetch a web page with retries.

        Args:
            url: URL to fetch

        Returns:
            HTML content of the page

        Raises:
            requests.RequestException: If unable to fetch the page
        """
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                
                # Try to detect encoding
                response.encoding = response.apparent_encoding
                return response.text
                
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise
                console.print(
                    f"[yellow]Retry {attempt + 1}/{self.max_retries} for {url}[/yellow]"
                )
                time.sleep(2 ** attempt)  # Exponential backoff
        
        raise requests.RequestException(f"Failed to fetch {url}")


# Made with Bob