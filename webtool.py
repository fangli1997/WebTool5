
#!/usr/bin/env python3
"""
Python Web Toolkit
A lightweight command-line website information and inspection tool.
"""

import argparse
import re
import sys
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


MAX_SIZE = 2 * 1024 * 1024
TIMEOUT = 15


class PageParser(HTMLParser):
    """Extract page title and links from HTML."""

    def __init__(self):
        super().__init__()
        self.title = ""
        self.links = []
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag.lower() == "title":
            self.in_title = True

        if tag.lower() == "a" and attrs.get("href"):
            self.links.append(attrs["href"])

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def validate_url(url):
    """Validate an HTTP or HTTPS URL."""
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError("Enter a valid HTTP or HTTPS URL.")

    if parsed.username or parsed.password:
        raise ValueError("URLs containing credentials are not supported.")

    return url


def fetch_page(url):
    """Fetch a webpage and return its content and headers."""
    validate_url(url)

    request = Request(
        url,
        headers={"User-Agent": "PythonWebToolkit/1.0"}
    )

    with urlopen(request, timeout=TIMEOUT) as response:
        content_type = response.headers.get("Content-Type", "")

        if "text/html" not in content_type.lower():
            raise ValueError("The URL does not return an HTML page.")

        content = response.read(MAX_SIZE + 1)

        if len(content) > MAX_SIZE:
            raise ValueError("Page exceeds the 2 MB download limit.")

        encoding = response.headers.get_content_charset() or "utf-8"

        return (
            response.status,
            response.headers,
            content.decode(encoding, errors="replace"),
            response.geturl()
        )


def inspect_website(url):
    """Display basic website information."""
    status, headers, html, final_url = fetch_page(url)

    parser = PageParser()
    parser.feed(html)

    parsed = urlparse(final_url)

    print("\n========== WEBSITE INFORMATION ==========")
    print(f"Requested URL : {url}")
    print(f"Final URL     : {final_url}")
    print(f"Domain        : {parsed.hostname}")
    print(f"Protocol      : {parsed.scheme.upper()}")
    print(f"Status Code   : {status}")
    print(f"Page Title    : {parser.title.strip() or 'Not found'}")
    print(f"Content Type  : {headers.get('Content-Type', 'Unknown')}")
    print(f"Server        : {headers.get('Server', 'Unknown')}")
    print(f"Page Size     : {len(html.encode('utf-8'))} bytes")
    print(f"Links Found   : {len(parser.links)}")

    print("\n========== EXTRACTED LINKS ==========")

    for index, link in enumerate(parser.links, 1):
        print(f"{index}. {urljoin(final_url, link)}")

    print("\n=========================================")


def check_status(url):
    """Check whether a website responds successfully."""
    try:
        status, headers, _, final_url = fetch_page(url)
        print(f"Website: {final_url}")
        print(f"Status: {status}")
        print(f"Server: {headers.get('Server', 'Unknown')}")
    except HTTPError as error:
        print(f"HTTP Error: {error.code} {error.reason}")
    except (URLError, TimeoutError, ValueError, OSError) as error:
        print(f"Error: {error}")


def main():
    parser = argparse.ArgumentParser(
        description="Python Web Toolkit - Inspect and extract website information."
    )

    parser.add_argument(
        "url",
        help="Website URL to inspect"
    )

    parser.add_argument(
        "-m", "--mode",
        choices=["inspect", "status"],
        default="inspect",
        help="Operation mode (default: inspect)"
    )

    args = parser.parse_args()

    try:
        if args.mode == "inspect":
            inspect_website(args.url)
        else:
            check_status(args.url)

    except HTTPError as error:
        print(f"HTTP Error: {error.code} {error.reason}")
        sys.exit(1)
    except (URLError, TimeoutError, ValueError, OSError) as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
