# Heimdall: Unauthenticated SSRF via test_config

## Description

Heimdall is a self-hosted application dashboard. Its SSRF guard was added to only one
controller. The enhanced-app test and live-stats path uses a raw HTTP client with no
validation. On a default (passwordless) install, `POST /test_config` is unauthenticated,
so anyone can make the server request arbitrary internal hosts and ports, including the
cloud metadata IP, with a status/port oracle in the response.

- Endpoint: `POST /test_config` (enhanced-app path)
- Privilege: none (default passwordless install)

## Exploit

`poc.py` (standard library only) loads an enhanced-app class, then makes the server
fetch your target and prints the oracle.

```
python3 poc.py --url http://localhost:8081 --target http://169.254.169.254/
```

## Disclaimer

This proof of concept is for authorized security testing and education only.
Test only systems that you own or have explicit permission to test. The author
takes no responsibility for misuse.
