"""
AI filtering pipeline for crowdsourced contributions.
Layers: spam → relevance → quality → score.
MVP version: simple keyword-based scoring.
Production: replace with BERT-based classifier.
"""
import re


# Domain keywords
RELEVANT_KEYWORDS = [
    'co2', 'carbon dioxide', 'methane', 'ch4', 'biogas', 'biomethane',
    'meg', 'monoethylene', 'glycol', 'solvent', 'absorption', 'solubility',
    'tio2', 'nanoparticle', 'nanofluid', 'amine', 'mdea', 'dea', 'mea',
    'pressure', 'temperature', 'bar', 'kelvin', 'separation', 'upgrading',
    'ccs', 'ccu', 'capture', 'storage', 'gas', 'liquid', 'equilibrium',
    'henry', 'peng-robinson', 'thermodynamic', 'kinetics',
    'box-behnken', 'response surface', 'regression', 'modeling',
]

SPAM_KEYWORDS = [
    'buy now', 'click here', 'viagra', 'casino', 'lottery',
    'make money fast', 'free crypto', 'work from home',
    'limited offer', 'act now', 'winner',
]


def score_contribution(title, description):
    """
    Score a contribution on a 0–100 scale.

    Returns:
        dict with keys: score, status, reasons, relevant_count, spam_count
    """
    text = f"{title} {description}".lower()

    # 1. Spam detection
    spam_count = sum(1 for kw in SPAM_KEYWORDS if kw in text)
    if spam_count >= 2:
        return {
            'score': 0,
            'status': 'rejected',
            'reasons': ['Multiple spam keywords detected'],
            'relevant_count': 0,
            'spam_count': spam_count
        }

    # 2. Relevance
    relevant_count = sum(1 for kw in RELEVANT_KEYWORDS if kw in text)

    # 3. Quality factors
    has_numbers = bool(re.search(r'\d+\.?\d*', text))
    has_units = bool(re.search(r'(bar|k|kelvin|mol|wt%|v/v|nm|°c)', text))
    has_reference = bool(re.search(r'(doi|http|et al|journal|paper|study|reference)', text))
    length_score = min(len(description) / 200, 1.0) * 20  # max 20

    # 4. Calculate score
    score = 0
    score += min(relevant_count * 8, 40)   # max 40 for relevance
    score += 15 if has_numbers else 0
    score += 10 if has_units else 0
    score += 10 if has_reference else 0
    score += length_score

    score = min(score, 100)

    # 5. Determine status
    if score >= 70:
        status = 'accepted'
        reasons = ['High relevance and quality']
    elif score >= 40:
        status = 'review'
        reasons = ['Moderate quality — needs human review']
    else:
        status = 'rejected'
        reasons = ['Insufficient relevance or quality']

    return {
        'score': round(score, 1),
        'status': status,
        'reasons': reasons,
        'relevant_count': relevant_count,
        'spam_count': spam_count
    }
