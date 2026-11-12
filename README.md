
# Python Web Toolkit

A lightweight command-line web inspection tool built using Python.

## Features

- Check website HTTP status codes.
- Extract website page titles.
- Extract and display website links.
- Display domain and protocol information.
- View server and content-type headers.
- Display downloaded page size.
- Support HTTP and HTTPS websites.
- No external Python dependencies.

## Requirements

- Python 3.8 or newer
- Internet connection

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/python-webtool.git
```

Navigate into the project:

```bash
cd python-webtool
```

No additional packages are required.

## Usage

### Inspect a website

```bash
python webtool.py https://example.com
```

### Check website status

```bash
python webtool.py https://example.com --mode status
```

### View available options

```bash
python webtool.py --help
```

## Project Structure

```text
python-webtool/
├── webtool.py
└── README.md
```

## Limitations

- Only HTML pages are supported in inspect mode.
- Downloads are limited to 2 MB.
- Website access depends on network connectivity.
- Some websites may block automated requests.

## Disclaimer

This tool is intended for educational purposes and
legitimate website inspection. Only inspect websites
you are authorized to access.

## License

MIT License
