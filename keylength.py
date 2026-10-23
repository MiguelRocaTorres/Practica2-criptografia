from measure import index_of_coincidence
THRESHOLDS = 0.6

def coset_ic(ciphertext: str, m: int) -> float:
    cosets = [ciphertext[i::m] for i in range(m)]
    total_ic = sum(index_of_coincidence(coset) for coset in cosets)
    return total_ic / m

def find_key_length(ciphertext: str, max_m: int = 16, language: str = "en") -> int:
    scores = {}
    for m in range(1, max_m + 1):
        ic = coset_ic(ciphertext, m)
        scores[m] = ic
        if ic >= THRESHOLDS:
            return m

    return max(scores, key = scores.get)