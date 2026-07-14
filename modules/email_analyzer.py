"""
===========================================================
ZEXXPHISH
Advanced Phishing Analyzer

File: email_analyzer.py

Description:
Analyzes email headers for phishing indicators.
===========================================================
"""

import re


SUSPICIOUS_DOMAINS = [
    "gmail.com",
    "yahoo.com",
    "outlook.com",
    "hotmail.com"
]


def analyze_email(header):

    findings = []
    score = 0

    sender = "Not Found"
    reply_to = "Not Found"
    return_path = "Not Found"

    spf = "Unknown"
    dkim = "Unknown"
    dmarc = "Unknown"

    sender_match = re.search(r"^From:\s*(.*)", header, re.MULTILINE | re.IGNORECASE)

    if sender_match:
        sender = sender_match.group(1).strip()

    reply_match = re.search(r"^Reply-To:\s*(.*)", header, re.MULTILINE | re.IGNORECASE)

    if reply_match:
        reply_to = reply_match.group(1).strip()

    return_match = re.search(r"^Return-Path:\s*(.*)", header, re.MULTILINE | re.IGNORECASE)

    if return_match:
        return_path = return_match.group(1).strip()

    if "spf=pass" in header.lower():
        spf = "PASS"
    elif "spf=fail" in header.lower():
        spf = "FAIL"
        findings.append("SPF authentication failed")
        score += 20

    if "dkim=pass" in header.lower():
        dkim = "PASS"
    elif "dkim=fail" in header.lower():
        dkim = "FAIL"
        findings.append("DKIM authentication failed")
        score += 20

    if "dmarc=pass" in header.lower():
        dmarc = "PASS"
    elif "dmarc=fail" in header.lower():
        dmarc = "FAIL"
        findings.append("DMARC authentication failed")
        score += 20

    if reply_to != "Not Found" and reply_to != sender:
        findings.append("Reply-To differs from sender")
        score += 15

    if return_path != "Not Found" and return_path != sender:
        findings.append("Return-Path differs from sender")
        score += 15

    sender_lower = sender.lower()

    for domain in SUSPICIOUS_DOMAINS:

        if sender_lower.endswith(domain):
            findings.append("Uses free email provider")
            score += 10
            break

    suspicious_words = [
        "verify",
        "urgent",
        "password",
        "bank",
        "account",
        "login",
        "security",
        "confirm"
    ]

    detected = []

    for word in suspicious_words:

        if word in header.lower():
            detected.append(word)

    if detected:

        findings.append(
            "Suspicious keywords: " + ", ".join(detected)
        )

        score += min(len(detected) * 5, 20)

    score = min(score, 100)

    if score <= 25:
        threat = "LOW"
        recommendation = "Email appears relatively safe."

    elif score <= 60:
        threat = "MEDIUM"
        recommendation = "Exercise caution before responding."

    else:
        threat = "HIGH"
        recommendation = "This email is highly suspicious."

    return {

        "sender": sender,
        "reply_to": reply_to,
        "return_path": return_path,
        "spf": spf,
        "dkim": dkim,
        "dmarc": dmarc,
        "risk_score": score,
        "threat_level": threat,
        "findings": findings,
        "recommendation": recommendation
    }


def display_email_report(result):

    print("\n" + "=" * 70)

    print(f"Sender         : {result['sender']}")
    print(f"Reply-To       : {result['reply_to']}")
    print(f"Return-Path    : {result['return_path']}")

    print()

    print(f"SPF            : {result['spf']}")
    print(f"DKIM           : {result['dkim']}")
    print(f"DMARC          : {result['dmarc']}")

    print()

    print(f"Risk Score     : {result['risk_score']}/100")
    print(f"Threat Level   : {result['threat_level']}")

    print("\nFindings:")

    if result["findings"]:

        for finding in result["findings"]:
            print(f" • {finding}")

    else:

        print(" • No suspicious indicators detected.")

    print("\nRecommendation:")

    print(result["recommendation"])

    print("=" * 70)