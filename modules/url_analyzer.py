"""
===========================================================
ZEXXPHISH
Advanced Phishing Analyzer

File: url_analyzer.py
===========================================================
"""

import re
import validators
import tldextract
from urllib.parse import urlparse
from modules.colors import Colors
from modules.scorer import calculate_risk

SUSPICIOUS_KEYWORDS = [
    "login", "verify", "update", "secure", "account",
    "password", "bank", "paypal", "signin",
    "confirm", "wallet", "gift", "free", "bonus"
]

URL_SHORTENERS = [
    "bit.ly",
    "tinyurl.com",
    "goo.gl",
    "t.co",
    "is.gd",
    "ow.ly",
    "cutt.ly",
    "rb.gy",
    "shorturl.at"
]


def analyze_url(url):

    url = url.strip()

    if not validators.url(url):
        return {
            "valid": False,
            "message": "Invalid URL."
        }

    parsed = urlparse(url)
    extracted = tldextract.extract(url)

    findings = []

    indicators = {
    "http": False,
    "ip": False,
    "shortener": False,
    "keywords": 0,
    "subdomains": False,
    "long_domain": False,
    "special_chars": False,
    "punycode": False
     }

    if parsed.scheme == "https":
        findings.append("HTTPS enabled")
    else:
        findings.append("Uses HTTP")
        indicators["http"] = True

    hostname = parsed.hostname or ""

    if re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", hostname):
        findings.append("Uses IP address")
        indicators["ip"] = True

    if hostname.lower() in URL_SHORTENERS:
        findings.append("URL shortener detected")
        indicators["shortener"] = True

    detected = []

    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in url.lower():
            detected.append(keyword)

    if detected:
        findings.append(
            "Suspicious keywords: " + ", ".join(detected)
        )
        indicators["keywords"] = len(detected)

    if extracted.subdomain:

        if len(extracted.subdomain.split(".")) >= 2:
            findings.append("Multiple subdomains detected")
            indicators["subdomains"] = True  

    if len(hostname) > 30:
        findings.append("Long domain")
        indicators["long_domain"] = True

    if url.count("-") + url.count("@") >= 3:
        findings.append("Many special characters")
        indicators["special_chars"] = True

    if "xn--" in hostname.lower():
        findings.append("Punycode detected")
        indicators["punycode"] = True


    score, threat, recommendation = calculate_risk(indicators)

    return {
        "valid": True,
        "url": url,
        "domain": extracted.registered_domain,
        "https": parsed.scheme == "https",
        "risk_score": score,
        "threat_level": threat,
        "findings": findings,
        "recommendation": recommendation
    }


def display_url_report(result):

    print("\n" + "=" * 70)

    if not result["valid"]:
        print(f"{Colors.RED}❌ {result['message']}{Colors.RESET}")
        return

    print(f"{Colors.CYAN}URL:{Colors.RESET}            {result['url']}")
    print(f"{Colors.CYAN}Domain:{Colors.RESET}         {result['domain']}")
    print(f"{Colors.CYAN}HTTPS:{Colors.RESET}          {'Yes' if result['https'] else 'No'}")
    print(f"{Colors.CYAN}Risk Score:{Colors.RESET}     {result['risk_score']}/100")

    if result["threat_level"] == "LOW":
        colour = Colors.GREEN
    elif result["threat_level"] == "MEDIUM":
        colour = Colors.YELLOW
    else:
        colour = Colors.RED

    print(
        f"{Colors.CYAN}Threat Level:{Colors.RESET}   "
        f"{colour}{result['threat_level']}{Colors.RESET}"
    )

    print("\nFindings:")

    if result["findings"]:
        for finding in result["findings"]:
            print(f" • {finding}")
    else:
        print(" • No suspicious indicators found.")

    print("\nRecommendation:")
    print(result["recommendation"])

    print("=" * 70)