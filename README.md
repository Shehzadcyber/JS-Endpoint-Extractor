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


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JS URL Extractor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #1e1e1e;
            color: #ffffff;
            margin: 0;
            padding: 0;
            text-align: center;
        }
        textarea {
            width: 80%;
            height: 200px;
            margin-top: 20px;
            background: #2e2e2e;
            color: #00ff99;
            border: 1px solid #555;
            padding: 10px;
            font-family: monospace;
            resize: vertical;
        }
        button {
            background-color: #00ff99;
            color: black;
            border: none;
            padding: 10px 20px;
            margin-top: 10px;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;
        }
        button:hover {
            background-color: #00cc7a;
        }
        #output {
            width: 80%;
            height: 200px;
            margin-top: 20px;
            background: #111;
            color: #ffcc00;
            border: 1px solid #555;
            padding: 10px;
            font-family: monospace;
            overflow-y: auto;
            text-align: left;
        }
    </style>
</head>
<body>
    <h1>JS URL Extractor</h1>
    <p>Paste your HTML or JavaScript code below:</p>
    <textarea id="inputCode" placeholder="Paste HTML/JS content here..."></textarea>
    <br>
    <button onclick="extractJS()">Extract .js URLs</button>

    <h2>Extracted JS URLs:</h2>
    <div id="output"></div>

    <script>
        function extractJS() {
            const input = document.getElementById("inputCode").value;
            const outputDiv = document.getElementById("output");

            // Regex to match .js URLs (handles relative & absolute paths)
            const regex = /(["'])(https?:\/\/[^\s"']+\.js|\/[^\s"']+\.js)(\?\S*)?\1/g;

            let matches = [];
            let match;
            while ((match = regex.exec(input)) !== null) {
                if (!matches.includes(match[2])) {
                    matches.push(match[2]);
                }
            }

            if (matches.length > 0) {
                outputDiv.innerHTML = matches.join("<br>");
            } else {
                outputDiv.innerHTML = "<i>No .js URLs found.</i>";
            }
        }
    </script>
</body>
</html>

