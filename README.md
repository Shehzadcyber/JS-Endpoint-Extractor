# JS-Endpoint-Extractor
JS Endpoint Extractor is a Python-based utility designed to scan .js files for potential API endpoints, helping security researchers, bug bounty hunters, and developers quickly uncover hidden or undocumented routes.

## Unlike basic regex scrapers, this tool:

  Fetches and analyzes JavaScript files one by one
  Extracts endpoints with high accuracy using multiple targeted regex patterns
  Supports authenticated scans via custom headers (Cookies, Tokens, etc.)
  Groups results by their origin .js file for better context
  Produces two outputs:
    Plain Text — grouped by origin with total unique endpoint count
    HTML Report — clean, clickable, browser-friendly format

# Features

Origin Tracking → Know exactly which .js file each endpoint came from.
Dual Output → Plain text & HTML report with clickable links.
Smart Regex Engine → Extracts absolute URLs, relative paths, REST-style endpoints, and query strings.
Authentication Support → Pass multiple headers (e.g., Cookie, Authorization) for restricted resources.
Temporary File Processing → Saves per-file results before merging & deduplication for maximum reliability.
Multi-Threading → Speed up large scans with concurrent fetching.

# Installation
```
git clone https://github.com/yourusername/js-endpoint-extractor.git
cd js-endpoint-extractor
pip install -r requirements.txt
```

# Usage
```
python3 extract.py \
  --input js-urls.txt \
  --output endpoints_output.txt \
  --headers "Cookie: AWSALBTG=abc123; Authorization: Bearer token" \
  --threads 5
```



