"""
===========================================================
ZEXXPHISH
Advanced Phishing Analyzer

File: scorer.py

Description:
Calculates URL risk score and threat level.
===========================================================
"""


def calculate_risk(indicators):
    """
    Calculates the final risk score.

    Parameters:
        indicators (dict)

    Returns:
        tuple(score, threat_level, recommendation)
    """

    score = 0

    if indicators["http"]:
        score += 20

    if indicators["ip"]:
        score += 25

    if indicators["shortener"]:
        score += 20

    score += min(indicators["keywords"] * 5, 25)

    if indicators["subdomains"]:
        score += 15

    if indicators["long_domain"]:
        score += 10

    if indicators["special_chars"]:
        score += 10

    if indicators["punycode"]:
        score += 25

    score = min(score, 100)

    if score <= 25:
        threat = "LOW"
        recommendation = "URL appears relatively safe."

    elif score <= 60:
        threat = "MEDIUM"
        recommendation = "Proceed carefully. Verify before visiting."

    else:
        threat = "HIGH"
        recommendation = "Avoid interacting with this URL."

    return score, threat, recommendation