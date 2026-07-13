#!/usr/bin/env python3
"""Regenerate sitemap.xml from the site's tracked HTML pages.

Run from the repo root. Discovers git-tracked *.html files, skips templates,
vendor samples, and the Google verification file, and writes sitemap.xml with a
per-page lastmod taken from each file's last git commit date.

This is invoked by .github/workflows/sitemap.yml on every push, so the sitemap
never needs to be hand-edited when a post is added.
"""

import subprocess
from datetime import date

BASE_URL = "https://ziyun-z.github.io/"

# Directories whose HTML is never a public page.
EXCLUDE_DIRS = ("assets/", "clarity/", "scripts/", ".github/")
# Exact basenames to skip.
EXCLUDE_BASENAMES = {"post-template.html"}


def is_excluded(path: str) -> bool:
    if any(path.startswith(d) for d in EXCLUDE_DIRS):
        return True
    base = path.rsplit("/", 1)[-1]
    if base in EXCLUDE_BASENAMES:
        return True
    if "template" in base:  # any other template partials
        return True
    # Google Search Console verification file, e.g. google0a4641c94930224e.html
    if base.startswith("google") and base.endswith(".html"):
        return True
    return False


def tracked_html() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "*.html"], capture_output=True, text=True, check=True
    ).stdout
    return [p for p in out.splitlines() if p and not is_excluded(p)]


def last_commit_date(path: str) -> str:
    """YYYY-MM-DD of the file's most recent commit; today if not yet committed."""
    out = subprocess.run(
        ["git", "log", "-1", "--date=short", "--format=%cd", "--", path],
        capture_output=True,
        text=True,
    ).stdout.strip()
    return out or date.today().isoformat()


def page_meta(path: str):
    """Return (loc_path, changefreq, priority) for a page path."""
    if path == "index.html":
        return "", "weekly", "1.0"
    if path.startswith("blog/"):
        return path, "yearly", "0.7"
    if path == "gallery.html":
        return path, "monthly", "0.5"
    return path, "monthly", "0.8"  # about.html and any future top-level page


def sort_key(path: str):
    # Home first, then non-blog top-level pages alphabetically, then blog posts
    # newest-first (by commit date), tie-broken by path.
    if path == "index.html":
        return (0, "", "")
    if path.startswith("blog/"):
        # negative-date sort: newest first
        return (2, _neg_date(last_commit_date(path)), path)
    return (1, path, "")


def _neg_date(d: str) -> str:
    # Invert a YYYY-MM-DD string so descending date sorts ascending.
    return "".join(str(9 - int(c)) if c.isdigit() else c for c in d)


def build() -> str:
    pages = sorted(tracked_html(), key=sort_key)
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path in pages:
        loc_path, changefreq, priority = page_meta(path)
        lines += [
            "    <url>",
            f"        <loc>{BASE_URL}{loc_path}</loc>",
            f"        <lastmod>{last_commit_date(path)}</lastmod>",
            f"        <changefreq>{changefreq}</changefreq>",
            f"        <priority>{priority}</priority>",
            "    </url>",
        ]
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(build())
    print("Wrote sitemap.xml")
