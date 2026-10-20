from collections import Counter

def index_of_coincidence(text: str) -> float:
    n = len(text)
    if n <= 1:
        return 0

    counts = Counter(text)
    numerator = sum(c * (c - 1) for c in counts.values())
    return round(numerator/ (n * (n - 1)), 4)

print(index_of_coincidence("CRYPTANALYSIS"))
print(index_of_coincidence("THEINDEXOFCOINCIDENCE"))