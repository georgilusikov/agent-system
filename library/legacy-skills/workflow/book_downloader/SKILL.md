---
skill_id: book_downloader
skill_name: Book Downloader
version: 1.0.0
category: workflow
triggers:
  - "download book"
  - "скачать книгу"
  - "annas archive"
  - "libgen"
dependencies: []
description: "Download books from Anna's Archive — search, select, and save to ~/Downloads/books."
---

# Book Downloader Skill

Download books from Anna's Archive using the browser (handles Cloudflare protection).

## Workflow

### Step 1: Get the book request from the user

Ask the user what book they want (title, author, preferred format: epub/pdf/any).

### Step 2: Search via browser

Use the `browser_subagent` to:

1. Navigate to `https://annas-archive.gs/search?q=QUERY` (fallback: `.se`, `.org`)
2. Wait for Cloudflare challenge to complete (the page auto-refreshes)
3. Read the search results — each result links to `/md5/HASH`
4. Extract: title, author, format, size, language from top 5-10 results

### Step 3: Present results to the user

Show the top 5 results and let the user pick (or auto-pick the best match).

### Step 4: Download via browser

Use `browser_subagent` to:

1. Navigate to the book's detail page (`/md5/HASH`)
2. Find the "slow download" link or an external mirror link
3. Click the download link
4. Wait for the download to complete

The browser downloads to the default downloads directory.

### Step 5: Move the file

Move the downloaded file from the browser's downloads dir to `~/Downloads/books/`:

```bash
mkdir -p ~/Downloads/books && mv ~/Downloads/FILENAME ~/Downloads/books/
```

### Step 6: Confirm to user

Report: file location, format, size.

## Domain Priority

Anna's Archive domains to try (the `.org` domain was suspended in Jan 2026):

1. `https://annas-archive.gs`
2. `https://annas-archive.se`
3. `https://annas-archive.org`

## Notes

- Direct HTTP (`requests`/`curl`) is blocked by Cloudflare JS challenge — **use browser only**
- The helper script at `scripts/download_book.py` is available but only works when Cloudflare is not active
- Supported formats: epub, pdf, mobi, azw3, fb2, djvu, cbr, cbz
