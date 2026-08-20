#!/usr/bin/env python3
"""
Book Downloader — search and download books from Anna's Archive.

Usage:
    python3 download_book.py search "QUERY" [--format epub|pdf|any] [--limit 10]
    python3 download_book.py download MD5 "filename.ext"

Output (search): JSON list of results
Output (download): saves file to ~/Downloads/books/
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.parse

import requests
from bs4 import BeautifulSoup

DOWNLOADS_DIR = os.path.expanduser("~/Downloads/books")
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

# Anna's Archive domains in priority order (.org was suspended Jan 2026)
DOMAINS = [
    "https://annas-archive.se",
    "https://annas-archive.gs",
    "https://annas-archive.org",
]
BASE_URL = DOMAINS[0]  # Default, overwritten by find_working_domain()

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}


def find_working_domain(session):
    """Try each domain and return the first working one."""
    for domain in DOMAINS:
        try:
            resp = session.get(domain, timeout=10, allow_redirects=True)
            if resp.status_code < 500:
                return domain
        except requests.RequestException:
            continue
    return DOMAINS[0]  # Fallback


def create_session():
    """Create a requests session with retry logic."""
    session = requests.Session()
    session.headers.update(HEADERS)
    adapter = requests.adapters.HTTPAdapter(
        max_retries=requests.adapters.Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
    )
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def search_books(query, ext_filter="", limit=10):
    """
    Search Anna's Archive and return structured results.
    """
    session = create_session()
    base_url = find_working_domain(session)

    params = {
        "q": query,
        "sort": "",
        "lang": "",
        "content": "",
    }
    if ext_filter and ext_filter != "any":
        params["ext"] = ext_filter

    url = f"{base_url}/search"

    try:
        resp = session.get(url, params=params, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(json.dumps({"error": f"Search request failed: {e}"}), file=sys.stderr)
        sys.exit(1)

    soup = BeautifulSoup(resp.text, "html.parser")
    results = []

    # Anna's Archive uses <a> tags with href="/md5/..." for search results
    result_links = soup.select('a[href*="/md5/"]')

    seen_md5 = set()
    for link in result_links:
        href = link.get("href", "")
        md5_match = re.search(r"/md5/([a-f0-9]{32})", href)
        if not md5_match:
            continue

        md5 = md5_match.group(1)
        if md5 in seen_md5:
            continue
        seen_md5.add(md5)

        # Extract text content from the link
        text_parts = link.get_text(separator="\n", strip=True).split("\n")
        text_parts = [p.strip() for p in text_parts if p.strip()]

        title = text_parts[0] if text_parts else "Unknown"

        # Try to extract metadata (author, format, size, language)
        author = ""
        file_format = ""
        file_size = ""
        language = ""

        full_text = link.get_text(separator=" ", strip=True)

        # Extract format from the text (epub, pdf, etc.)
        fmt_match = re.search(
            r"\b(epub|pdf|mobi|azw3?|fb2|djvu|cbr|cbz|doc|docx|txt|rtf)\b",
            full_text,
            re.IGNORECASE,
        )
        if fmt_match:
            file_format = fmt_match.group(1).lower()

        # Extract size
        size_match = re.search(
            r"(\d+(?:\.\d+)?\s*(?:KB|MB|GB|B)\b)", full_text, re.IGNORECASE
        )
        if size_match:
            file_size = size_match.group(1)

        # Extract language
        lang_match = re.search(
            r"\b(English|Russian|Spanish|French|German|Chinese|Japanese|"
            r"Italian|Portuguese|Dutch|Korean|Arabic|Hindi|Turkish|Polish|"
            r"Czech|Swedish|Norwegian|Danish|Finnish|Ukrainian|"
            r"Русский|Английский)\b",
            full_text,
            re.IGNORECASE,
        )
        if lang_match:
            language = lang_match.group(1)

        # Try to find author from structured parts
        for part in text_parts[1:]:
            if not re.search(r"\d+\s*(KB|MB|GB)\b", part, re.IGNORECASE) and \
               not re.search(r"\b(epub|pdf|mobi|azw3?)\b", part, re.IGNORECASE) and \
               len(part) > 2 and len(part) < 100:
                if not author:
                    author = part
                break

        results.append({
            "md5": md5,
            "title": title,
            "author": author,
            "format": file_format,
            "size": file_size,
            "language": language,
            "url": f"{base_url}{href}",
        })

        if len(results) >= limit:
            break

    return results


def get_download_links(md5):
    """
    Get download links for a given MD5 hash from the book detail page.
    Returns a list of download URLs.
    """
    session = create_session()
    base_url = find_working_domain(session)
    detail_url = f"{base_url}/md5/{md5}"

    try:
        resp = session.get(detail_url, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(json.dumps({"error": f"Detail page request failed: {e}"}), file=sys.stderr)
        return []

    soup = BeautifulSoup(resp.text, "html.parser")

    download_links = []

    # Look for download links — Anna's Archive shows multiple mirrors
    # Common patterns: links containing "download", "/slow_download/", external mirrors
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        text = a_tag.get_text(strip=True).lower()

        # Look for slow download links (direct from AA)
        if "/slow_download/" in href:
            full_url = href if href.startswith("http") else f"{base_url}{href}"
            download_links.append({"url": full_url, "source": "annas-archive-slow", "label": a_tag.get_text(strip=True)})

        # Look for external mirror links
        elif any(mirror in href for mirror in [
            "libgen", "library.lol", "z-lib", "sci-hub", "ipfs",
            "cloudflare-ipfs", "pinata", "dweb.link"
        ]):
            download_links.append({"url": href, "source": "mirror", "label": a_tag.get_text(strip=True)})

        # General download links
        elif "download" in text and href.startswith("http"):
            download_links.append({"url": href, "source": "direct", "label": a_tag.get_text(strip=True)})

    return download_links


def follow_download_link(url, session):
    """Follow a download link, handling redirects, and return the final response."""
    try:
        resp = session.get(url, timeout=60, stream=True, allow_redirects=True)
        resp.raise_for_status()

        # Check if we got HTML (need to parse further) or actual file
        content_type = resp.headers.get("Content-Type", "")
        if "text/html" in content_type:
            # This is a download page, look for the actual link
            body = resp.content
            soup = BeautifulSoup(body, "html.parser")

            # Look for download button/link
            for a in soup.find_all("a", href=True):
                link_text = a.get_text(strip=True).lower()
                href = a["href"]
                if "download" in link_text or "get" in link_text:
                    if href.startswith("http"):
                        return session.get(href, timeout=120, stream=True, allow_redirects=True)

            return None

        return resp
    except requests.RequestException:
        return None


def download_book(md5, filename):
    """
    Download a book by MD5 hash and save it to disk.
    """
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)

    session = create_session()
    links = get_download_links(md5)

    if not links:
        print(json.dumps({"error": "No download links found"}), file=sys.stderr)
        sys.exit(1)

    filepath = os.path.join(DOWNLOADS_DIR, filename)

    # Try slow download first (most reliable), then mirrors
    sorted_links = sorted(links, key=lambda x: 0 if "slow" in x["source"] else 1)

    for link_info in sorted_links:
        url = link_info["url"]
        source = link_info["source"]

        print(f"Trying {source}: {url[:80]}...", file=sys.stderr)

        try:
            resp = follow_download_link(url, session)
            if resp is None:
                continue

            content_type = resp.headers.get("Content-Type", "")
            content_length = resp.headers.get("Content-Length", "0")

            # Verify we got a binary file
            if "text/html" in content_type and int(content_length or 0) < 10000:
                print(f"  Got HTML page instead of file, skipping...", file=sys.stderr)
                continue

            total = int(content_length) if content_length else 0
            downloaded = 0

            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total > 0:
                        pct = int(downloaded / total * 100)
                        print(f"\r  Progress: {pct}% ({downloaded}/{total})", end="", file=sys.stderr)

            print(file=sys.stderr)

            # Basic sanity check: file should be > 1KB
            if os.path.getsize(filepath) < 1024:
                print(f"  Downloaded file too small, skipping...", file=sys.stderr)
                os.remove(filepath)
                continue

            print(json.dumps({
                "success": True,
                "path": filepath,
                "size": os.path.getsize(filepath),
                "source": source,
            }))
            return

        except Exception as e:
            print(f"  Failed: {e}", file=sys.stderr)
            if os.path.exists(filepath):
                os.remove(filepath)
            continue

    print(json.dumps({"error": "All download attempts failed"}), file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Anna's Archive Book Downloader")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search for books")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument(
        "--format", "-f",
        default="",
        help="Filter by format (epub, pdf, or empty for any)",
    )
    search_parser.add_argument(
        "--limit", "-l",
        type=int,
        default=10,
        help="Max number of results (default: 10)",
    )

    # Download command
    dl_parser = subparsers.add_parser("download", help="Download a book by MD5")
    dl_parser.add_argument("md5", help="MD5 hash of the book")
    dl_parser.add_argument("filename", help="Output filename (e.g. 'book.epub')")

    # Links command (get download links without downloading)
    links_parser = subparsers.add_parser("links", help="Get download links for MD5")
    links_parser.add_argument("md5", help="MD5 hash of the book")

    args = parser.parse_args()

    if args.command == "search":
        results = search_books(args.query, ext_filter=args.format, limit=args.limit)
        print(json.dumps(results, ensure_ascii=False, indent=2))

    elif args.command == "download":
        download_book(args.md5, args.filename)

    elif args.command == "links":
        links = get_download_links(args.md5)
        print(json.dumps(links, ensure_ascii=False, indent=2))

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
