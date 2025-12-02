#!/usr/bin/env python3
"""
breach.py — LeakCheck public API email breach checker
with neon/glitch banner and typing animation.

Powered by LeakCheck (https://leakcheck.io)
"""

import re
import sys
import json
import time
import random
import argparse
import requests
from typing import Dict, Any

# =========================
# CONFIG — LeakCheck Public API
# =========================
LEAKCHECK_PUBLIC_URL = "https://leakcheck.io/api/public"

# =========================
# COLORS
# =========================
RESET   = "\033[0m"
RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
CYAN    = "\033[96m"
MAGENTA = "\033[95m"

# Neon palette for glitch effect
NEON_COLORS = [CYAN, MAGENTA, YELLOW, GREEN]

# =========================
# BANNER TEXT (no colors here)
# =========================
BANNER_TEXT = r"""
 _______   _______   ________   ______    ______   __    __ 
/       \ /       \ /        | /      \  /      \ /  |  /  |
$$$$$$$  |$$$$$$$  |$$$$$$$$/ /$$$$$$  |/$$$$$$  |$$ |  $$ |
$$ |__$$ |$$ |__$$ |$$ |__    $$ |__$$ |$$ |  $$/ $$ |__$$ |
$$    $$< $$    $$< $$    |   $$    $$ |$$ |      $$    $$ |
$$$$$$$  |$$$$$$$  |$$$$$/    $$$$$$$$ |$$ |   __ $$$$$$$$ |
$$ |__$$ |$$ |  $$ |$$ |_____ $$ |  $$ |$$ \__/  |$$ |  $$ |
$$    $$/ $$ |  $$ |$$       |$$ |  $$ |$$    $$/ $$ |  $$ |
$$$$$$$/  $$/   $$/ $$$$$$$$/ $$/   $$/  $$$$$$/  $$/   $$/ 
"""

# =========================
# FANCY BANNER PRINTING
# =========================

def type_glitch_line(line: str, char_delay: float = 0.0015) -> None:
    """Print one line with neon/glitch typing effect."""
    for ch in line:
        if ch.strip() == "":
            # spaces stay uncolored to keep shape clean
            sys.stdout.write(ch)
        else:
            color = random.choice(NEON_COLORS)
            sys.stdout.write(color + ch + RESET)
        sys.stdout.flush()
        time.sleep(char_delay)
    sys.stdout.write("\n")


def show_banner() -> None:
    """Show full BREACH banner with typing + neon glitch effect."""
    sys.stdout.write("\n")
    for line in BANNER_TEXT.splitlines():
        if not line.strip():
            sys.stdout.write("\n")
            continue
        type_glitch_line(line)
    sys.stdout.write("\n")

    # Typing animation for signature
    sig = "made by xycaerys  |  powered by LeakCheck.io"
    sys.stdout.write(CYAN)
    for ch in sig:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(0.03)
    sys.stdout.write(RESET + "\n\n")
    sys.stdout.flush()

# =========================
# HELPERS
# =========================

def is_valid_email(email: str) -> bool:
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None


def call_leakcheck(email: str) -> Dict[str, Any]:
    """
    Calls LeakCheck public API:
      GET https://leakcheck.io/api/public?check=<email>

    Expected JSON (from docs):
    {
        "success": true,
        "found": 3,
        "fields": ["username", "first_name", "address"],
        "sources": [
            {"name": "Evony.com", "date": "2016-07"},
            ...
        ]
    }
    """
    if not is_valid_email(email):
        return {"error": "Invalid email format"}

    params = {"check": email}

    try:
        resp = requests.get(LEAKCHECK_PUBLIC_URL, params=params, timeout=15)
    except Exception as e:
        return {"error": f"Network error: {e}"}

    if resp.status_code != 200:
        return {"error": f"LeakCheck HTTP {resp.status_code} response"}

    try:
        data = resp.json()
    except Exception:
        return {"error": "Invalid JSON response from LeakCheck"}

    if not isinstance(data, dict):
        return {"error": "Unexpected response format from LeakCheck"}

    # Handle success flag
    if not data.get("success", False):
        # Some errors may not have more info, so be generic
        return {"error": "LeakCheck returned success = false (no data or invalid query)"}

    found = data.get("found", 0)
    fields = data.get("fields", []) or []
    sources = data.get("sources", []) or []

    breaches = []
    for s in sources:
        breaches.append({
            "name": s.get("name") or "Unknown",
            "date": s.get("date") or "Unknown",
            "exposed_data": fields if isinstance(fields, list) else [str(fields)],
        })

    return {
        "email": email,
        "breach_count": int(found) if isinstance(found, int) else len(breaches),
        "breaches": breaches,
        "raw": data,
    }

# =========================
# OUTPUT FORMATTING
# =========================

def print_human(result: Dict[str, Any]):
    if "error" in result:
        print(f"{RED}[ERROR]{RESET} {result['error']}")
        return

    email = result["email"]
    count = result["breach_count"]
    breaches = result["breaches"]

    if count == 0 or not breaches:
        print(f"{GREEN}[OK]{RESET} No breaches found for {CYAN}{email}{RESET}")
        return

    print(f"{YELLOW}[!]{RESET} Breaches found for {CYAN}{email}{RESET}: {YELLOW}{count}{RESET}")
    print("-" * 60)

    for i, b in enumerate(breaches, 1):
        name = b.get("name", "Unknown")
        date = b.get("date", "Unknown")
        exposed = b.get("exposed_data") or []
        if isinstance(exposed, list):
            exposed_str = ", ".join(exposed)
        else:
            exposed_str = str(exposed)

        print(f"{CYAN}{i}. {name}{RESET}")
        print(f"   Date        : {date}")
        print(f"   Exposed Data: {exposed_str}")
        print("-" * 60)

# =========================
# MAIN CLI
# =========================

def main():
    show_banner()

    parser = argparse.ArgumentParser(description="LeakCheck Public Breach Checker CLI")
    # email is optional on the command line; if missing, we will prompt
    parser.add_argument("email", nargs="?", help="Email to search")
    parser.add_argument("--json", action="store_true", help="Raw JSON output")
    args = parser.parse_args()

    email = args.email
    if not email:
        email = input(f"{YELLOW}[?]{RESET} Enter email to check: ").strip()

    result = call_leakcheck(email)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_human(result)


if __name__ == "__main__":
    main()
