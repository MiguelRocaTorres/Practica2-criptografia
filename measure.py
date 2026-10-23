from collections import Counter

def index_of_coincidence(text: str) -> float:
    n = len(text)
    if n <= 1:
        return 0

    counts = Counter(text)
    numerator = sum(c * (c - 1) for c in counts.values())
    return round(numerator/ (n * (n - 1)), 4)

#print(index_of_coincidence("CRYPTANALYSIS"))
#print(index_of_coincidence("THEINDEXOFCOINCIDENCE"))

#SACADO DE WIKIPEDIA
FREQS = {"en": {'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
    'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153,
    'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
    'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974,
    'Z': 0.00074}}

THRESHOLDS = 0.6

def classify(ciphertext: str, language: str = "en") -> str:
    """Return "transposition" or "substitution"."""
    n = len(ciphertext)
    if n == 0:
        return "substitution"

    counts = Counter(ciphertext)
    probs = FREQS.get(language, FREQS["en"])
    chi2 = sum(((counts[char] - n * p) ** 2) / (n * p) for char, p in probs.items())
    norm_chi2 = chi2 / n

    return "transposition" if norm_chi2 < THRESHOLDS else "substitution"