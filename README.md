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



## 🚀 Tech & Tools

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)
![NestJS](https://img.shields.io/badge/NestJS-E0234E?style=for-the-badge&logo=nestjs&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

## 📊 GitHub Stats

![GitHub Stats](https://github-readme-stats.vercel.app/api?username=shehzadcyber&show_icons=true&theme=tokyonight)
![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=shehzadcyber&layout=compact&theme=tokyonight)

## 🔥 Streak

[![GitHub Streak](https://streak-stats.demolab.com?user=shehzadcyber&theme=tokyonight)](https://git.io/streak-stats)


