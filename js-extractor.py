import argparse
import concurrent.futures
import os
import re
import sys
import time
import hashlib
from typing import Dict, Iterable, List, Set, Tuple
from urllib.parse import urljoin

try:
    from colorama import init as colorama_init, Fore, Style
    colorama_init(autoreset=True)
except Exception:
    class _Dummy:
        def __getattr__(self, name):
            return ''
    Fore = Style = _Dummy()

try:
    import requests
except ImportError:
    print("requests is required: pip install requests")
    sys.exit(1)

BANNER = f"""
{Fore.CYAN}{Style.BRIGHT}┌──────────────────────────────────────────────────────────┐
│                  JS Endpoint Extractor                   │
│              with Origins & Deduplication                │
│         Author: TheRoyHunter313  🛡️                       │
│ X: https://x.com/TheRoyHunter313                         │
│ LinkedIn: https://www.linkedin.com/in/shehzadali1337/    │
└──────────────────────────────────────────────────────────┘{Style.RESET_ALL}
"""

HEADER_BLOCK_RE = re.compile(r"([A-Za-z0-9\-]+)\s*:\s*(.*?)(?=(?:[A-Za-z0-9\-]+\s*:)|\Z)", re.DOTALL)

def parse_headers(header_str: str) -> Dict[str, str]:
    headers: Dict[str, str] = {}
    if not header_str:
        return headers
    for m in HEADER_BLOCK_RE.finditer(header_str.strip()):
        name = m.group(1).strip()
        val  = m.group(2).strip()
        if not name:
            continue
        headers[name] = re.sub(r"\s+", " ", val)
    return headers

ABS_URL_RE   = re.compile(r"https?://[^\s'\"<>)]+", re.IGNORECASE)
PR_URL_RE    = re.compile(r"(?<!:)//[A-Za-z0-9.-]+(?:/[\w\-._~%!$&'()*+,;=:@/?#]*)?", re.IGNORECASE)
PATH_RE      = re.compile(r"(?<![A-Za-z0-9_])(\/(?:(?:api|v\d+|auth|user|users|admin|account|login|logout|session|data|graph|svc|service|rest|oauth)[\w\-./]*|[\w\-./]+))(?:\?[\w\-._~%!$&'()*+,;=:@/?#]*)?", re.IGNORECASE)
REL_PATH_RE  = re.compile(r"\.{1,2}\/[\w\-./]+(?:\?[\w\-._~%!$&'()*+,;=:@/?#]*)?", re.IGNORECASE)
STRINGED_RE  = re.compile(r"[\"'`](https?:\/\/[^\"'`<>\s]+|\/[^\"'`<>\s]+|\.\.?\/[^\"'`<>\s]+)[\"'`]")

TRAILING_TRIM = re.compile(r"[\s\"'`,);]+$")

def normalize_endpoint(raw: str) -> str:
    s = raw.strip()
    s = TRAILING_TRIM.sub('', s)
    if s.startswith('///'):
        while s.startswith('///'):
            s = s[1:]
    return s

def extract_endpoints(js_text: str) -> Set[str]:
    found: Set[str] = set()
    for regex in (ABS_URL_RE, PR_URL_RE, STRINGED_RE, PATH_RE, REL_PATH_RE):
        for m in regex.findall(js_text):
            candidate = m[0] if isinstance(m, tuple) else m
            ep = normalize_endpoint(candidate)
            if ep:
                found.add(ep)
    return found

def fetch_js(url: str, headers: Dict[str, str], timeout: int = 20, retries: int = 2) -> Tuple[str, str]:
    sess = requests.Session()
    merged_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
        **(headers or {})
    }
    last_exc = None
    for attempt in range(retries + 1):
        try:
            resp = sess.get(url, headers=merged_headers, timeout=timeout)
            if resp.status_code >= 400:
                raise requests.HTTPError(f"HTTP {resp.status_code}")
            resp.encoding = resp.encoding or 'utf-8'
            return url, resp.text
        except Exception as e:
            last_exc = e
            if attempt < retries:
                time.sleep(0.7 * (attempt + 1))
            else:
                raise last_exc

def safe_temp_dir(base: str = ".endpoints_tmp") -> str:
    os.makedirs(base, exist_ok=True)
    return base

def temp_filename_for(url: str, tmpdir: str) -> str:
    h = hashlib.sha1(url.encode('utf-8')).hexdigest()[:12]
    return os.path.join(tmpdir, f"{h}.txt")

def write_lines(path: str, lines: Iterable[str]) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        for line in sorted(set(l.strip() for l in lines if l.strip())):
            f.write(line + "\n")

def load_urls(path: str) -> List[str]:
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def process_single(url: str, headers: Dict[str, str], tmpdir: str, timeout: int, retries: int) -> Tuple[str, Set[str]]:
    content = fetch_js(url, headers=headers, timeout=timeout, retries=retries)[1]
    eps = extract_endpoints(content)
    write_lines(temp_filename_for(url, tmpdir), eps)
    return url, eps

def merge_temp_with_origins(urls: List[str], tmpdir: str) -> Dict[str, Set[str]]:
    result: Dict[str, Set[str]] = {}
    for url in urls:
        p = temp_filename_for(url, tmpdir)
        if not os.path.exists(p):
            continue
        with open(p, 'r', encoding='utf-8') as f:
            result[url] = set(line.strip() for line in f if line.strip())
    return result

def save_html(origins: Dict[str, Set[str]], html_path: str) -> None:
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write("<!DOCTYPE html>\n<html>\n<head>\n")
        f.write("<meta charset='utf-8'>\n<title>JS Endpoint Extractor Report</title>\n")
        f.write("<style>body{font-family:Arial,sans-serif;background:#f9f9f9;color:#222;}"
                "h2{color:#007acc;}ul{list-style-type:square;}"
                "a{text-decoration:none;color:#333;}a:hover{color:#d14;}</style>\n")
        f.write("</head>\n<body>\n")
        f.write("<h1>JS Endpoint Extractor Report</h1>\n")
        f.write("<p>Author: TheRoyHunter313<br>"
                "X: <a href='https://x.com/TheRoyHunter313'>https://x.com/TheRoyHunter313</a><br>"
                "LinkedIn: <a href='https://www.linkedin.com/in/shehzadali1337/'>https://www.linkedin.com/in/shehzadali1337/</a></p>\n")

        total_count = sum(len(eps) for eps in origins.values())
        f.write(f"<p><strong>Total Unique Endpoints:</strong> {total_count}</p>\n")

        for origin, eps in origins.items():
            if not eps:
                continue
            f.write(f"<h2>Origin: {origin}</h2>\n<ul>\n")
            for ep in sorted(eps):
                if ep.startswith("http"):
                    link = ep
                else:
                    link = urljoin(origin, ep)
                f.write(f"<li><a href='{link}' target='_blank'>{ep}</a></li>\n")
            f.write("</ul>\n")

        f.write("</body>\n</html>")

def main():
    print(BANNER)
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--headers', default='')
    ap.add_argument('--timeout', type=int, default=20)
    ap.add_argument('--retries', type=int, default=2)
    ap.add_argument('--tmpdir', default='.endpoints_tmp')
    ap.add_argument('--threads', type=int, default=1)
    args = ap.parse_args()

    headers = parse_headers(args.headers)
    urls = load_urls(args.input)
    if not urls:
        print(f"{Fore.YELLOW}No URLs found in {args.input}{Style.RESET_ALL}")
        sys.exit(1)

    tmpdir = safe_temp_dir(args.tmpdir)

    def _worker(u: str):
        try:
            return process_single(u, headers, tmpdir, args.timeout, args.retries)
        except Exception as e:
            print(f"{Fore.RED}Failed: {u} ({e}){Style.RESET_ALL}")
            return u, set()

    if args.threads == 1:
        for idx, u in enumerate(urls, 1):
            print(f"[{idx}/{len(urls)}] {Fore.CYAN}Processing: {u}{Style.RESET_ALL}")
            _worker(u)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as ex:
            list(ex.map(_worker, urls))

    origins = merge_temp_with_origins(urls, tmpdir)
    unique_eps: Set[str] = set(ep for eps in origins.values() for ep in eps)

    # Save plain text
    with open(args.output, 'w', encoding='utf-8') as f:
        for origin, eps in origins.items():
            if eps:
                f.write(f"Origin: {origin}\n")
                for ep in sorted(eps):
                    f.write(ep + "\n")
                f.write("\n")
        f.write(f"Total Unique Endpoints: {len(unique_eps)}\n")

    # Save HTML
    html_output_path = args.output + ".html"
    save_html(origins, html_output_path)

    print(f"{Fore.GREEN}{len(unique_eps)} unique endpoints saved to {args.output} and {html_output_path}{Style.RESET_ALL}")

if __name__ == '__main__':
    main()
