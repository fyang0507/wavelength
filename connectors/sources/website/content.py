"""
[GENERATED BY CURSOR]
Script to crawl website content, generate a summary using LLM, and estimate reading time.
Combines functionality from website scraping, LLM summarization, and reading time estimation.
"""

from utils.logging_config import logger
import tomllib
from pathlib import Path
from services.llm import api_text_completion
from connectors.sources.website.scrapers import get_scraper
from connectors.sources.website.parsers import get_parser
from utils.read_time_estimate import estimate_read_time
from utils.llm_response_format import parse_bullet_points
from typing import Optional, Dict, Any


def scrape_and_process_content(url: str, scraper_type: str, content_parser: str) -> Optional[Dict[str, Any]]:
    """
    Scrapes a website, parses the content, generates a summary, and estimates reading time.
    
    Args:
        url: The URL of the website to scrape
        scraper_type: The type of scraper to use ("basic" or "playwright")
        content_parser: Name of the parser to use (e.g., "36kr", "generic"). 
        
    Returns:
        dict: Dictionary containing the scraped content, summary, and read time, or None if error
    """
    try:        
        # Step 1: Scrape the content
        scraper = get_scraper(scraper_type)
        if not scraper:
            logger.error(f"Failed to get scraper for type: {scraper_type} for url {url}")
            return None 
        
        html_content = scraper.scrape(url)
        if not html_content:
            logger.error(f"Failed to scrape content from {url} using {scraper_type} scraper.")
            return None

        parser = get_parser(content_parser)
        if not parser:
            error_msg = f"Fatal: Could not get any parser instance {content_parser} for {url}."
            logger.error(error_msg)
            return None
        
        logger.info(f"Processing content for {url} using scraper: {scraper_type}, parser: {content_parser}")
        
        # Parse content using the obtained parser
        parsed_data: Optional[Dict[str, str]] = None
        try:
            logger.info(f"Using '{content_parser}' parser instance's extract_content method for {url}.")
            parsed_data = parser.extract_content(html_content)
            if parsed_data:
                logger.success(f"Successfully parsed content using parser: {content_parser}")
            else:
                logger.warning(f"Parser '{content_parser}' returned None for content from {url}.")
        except Exception as e:
            logger.error(f"Error calling '{content_parser}' parser's extract_content: {e}", exc_info=True)
            # parsed_data will be None or its previous state. The critical check below handles it.

        # Ensure we have critical fields from parsed_data
        if not parsed_data or not parsed_data.get('title') or not parsed_data.get('content'):
            logger.error(f"Critical data ('title' or 'content') missing from parser '{content_parser}' output for {url}. Parser returned: {parsed_data}")
            return None
            
        # Step 2: Generate summary using LLM
        raw_summary = summarize_content(parsed_data['content'])
        summary = parse_bullet_points(raw_summary) if raw_summary else None
        if not summary:
            logger.warning(f"Failed to generate or parse summary for {url}")
        
        # Step 3: Estimate reading time
        read_time = estimate_read_time(parsed_data['content'])
        
        result = {
            "url": url,
            "title": parsed_data['title'],
            "html_content": html_content, # Still useful to save the raw HTML
            "content": parsed_data['content'],
            "summary": summary,
            "read_time": read_time
        }
        
        logger.success(f"Successfully processed content from {url} (Parser: {content_parser})")
        logger.info(f"Title: {result['title']}")
        logger.info(f"Reading time: {result['read_time']}")
        
        return result
        
    except Exception as e:
        # Catch-all for unexpected errors in the main try block of scrape_and_process_content
        logger.error(f"Overall error processing content from {url}: {e}", exc_info=True)
        return None


def summarize_content(content: str) -> Optional[str]:
    """
    Generates a summary of the content using LLM.
    Args:
        content: The content to summarize
    Returns:
        str: The summary text, or None if error
    """
    try:
        prompt_file_path = Path("prompts/website.toml")
        if not prompt_file_path.exists():
            logger.error(f"Prompt file not found: {prompt_file_path}")
            return None
            
        with open(prompt_file_path, "rb") as f:
            prompts = tomllib.load(f)
        
        system_prompt = prompts['summary']['system']
        model = prompts['summary']['model']
        
        logger.info(f"Generating summary using LLM (model: {model}) for content snippet: {content[:100]}...")
        
        response = api_text_completion(
            model=model,
            system_prompt=system_prompt,
            user_message=content
        )
        
        logger.success(f"Successfully generated summary.") # Removed response from log for brevity
        return response
    
    except Exception as e:
        logger.error(f"Error generating summary: {e}", exc_info=True)
        return None


def save_processed_content(result, output_dir):
    """
    Saves processed content to files.
    Args:
        result: Dictionary containing processed content
        output_dir: Directory to save files to
    Returns:
        bool: True if successful, False if error
    """
    if result["title"]:
        filename = "".join(c if c.isalnum() or c in [' ', '_', '-'] else '_' for c in result["title"])
        filename = filename.replace(' ', '_')[:50]
    else:
        import hashlib
        filename = hashlib.md5(result["url"].encode()).hexdigest()[:10]
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    markdown_path = output_path / f"{filename}.md"
    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write(f"# {result['title']}\n\n")
        f.write(f"URL: {result['url']}\n")
        f.write(f"Reading time: {result['read_time']}\n\n")
        f.write("## Summary\n\n")
        f.write(f"{result.get('summary', 'N/A')}\n\n") # Use .get for summary
        f.write("## Content\n\n")
        f.write(result['content'])
    
    html_path = output_path / f"{filename}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(result['html_content'])
    
    logger.success(f"Content saved to {markdown_path} and {html_path}")


def main():
    """Main function with placeholder values."""
    target_url = "https://36kr.com/p/3232982907338757"
    scraper_to_use = "playwright"
    parser_to_use = "36kr" 
    output_dir = "data/36kr"
    
    logger.info(f"Running main content processing for URL: {target_url}, Scraper: {scraper_to_use}, Parser: {parser_to_use if parser_to_use else 'generic'}")
    
    result = scrape_and_process_content(
        url=target_url,
        scraper_type=scraper_to_use,
        content_parser=parser_to_use # Pass the string name
    )
    
    if result:
        save_processed_content(result, output_dir=output_dir)
        logger.info(f"Article: {result['title']}")
        logger.info(f"Reading time: {result['read_time']}")

        # Ensure summary is a string before slicing
        summary_display = result.get('summary', 'N/A')
        if not isinstance(summary_display, str):
            summary_display = str(summary_display)
        logger.info(f"Summary: {summary_display[:150]}...")
    else:
        logger.error(f"Failed to process content from {target_url}")


if __name__ == "__main__":
    main()
