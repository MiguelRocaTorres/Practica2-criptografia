from collections import defaultdict
def clean(text: str) -> str:
    return "".join(c for c in text.upper() if "A" <= c <= "Z")

def repeats(ciphertext: str, min_len: int = 3) -> dict[str, list[int]]:
    text = clean(ciphertext)
    n = len(text)
    result = {}
    for length in range(min_len, n + 1):
        occurrences = defaultdict(list)
        for i in range(n -length + 1):
            sub = text[i: i + length]
            occurrences[sub].append(i)

        for sub, positions in occurrences.items():
            if len(positions) > 1:
                result[sub] = positions

    return result

def distances(ciphertext: str, min_len: int = 3) -> list[int]:
    rep = repeats(ciphertext, min_len)
    dists = set()
    for positions in rep.values():
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                dists.add(positions[j] - positions[i])

    return sorted(dists)

def factor_tally(ciphertext: str, max_factor: int = 20) -> dict[int, int]:
    dists = distances(ciphertext)
    tally = {f: 0 for f in range(2, max_factor + 1)}
    for d in dists:
        for f in range(2, max_factor + 1):
            if d % f == 0:
                tally[f] += 1

    return tally

ciphertext = sample = """
ELQYR JVQDR LXEGB ELQQV ALQFE PTQOG DEZRG SIDSC PEFGO PXDOL
ELQYR JXADA LPKGV D
"""

print(repeats(ciphertext), "\n")
print(distances(ciphertext), "\n")
print(factor_tally(ciphertext))