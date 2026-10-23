from collections import Counter
import itertools
import math

CORPUS_EN = (
    "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG THIS IS A SAMPLE TEXT FOR "
    "FREQUENCY ANALYSIS IN CRYPTOGRAPHY TRANSPOSITION CIPHERS DO NOT CHANGE "
    "THE LETTERS BUT REORDER THEM CAUSING BIGRAM FREQUENCIES TO BE PRESERVED "
    "IN THE CORRECT ORDER AND DESTROYED IN WRONG PERMUTATIONS OF COLUMNS"
)


def _get_bigram_model(corpus: str = CORPUS_EN) -> dict[tuple[str, str], float]:
    clean = "".join(c for c in corpus.upper() if "A" <= c <= "Z")
    counts = Counter(zip(clean, clean[1:]))
    total = sum(counts.values()) + 26 * 26  
    alphabet = [chr(i + ord("A")) for i in range(26)]
    return {
        (c1, c2): math.log((counts[(c1, c2)] + 1) / total)
        for c1 in alphabet
        for c2 in alphabet
    }


BIGRAMS = _get_bigram_model()


def attack(ciphertext: str, n_cols: int, language: str = "en") -> tuple[tuple[int, ...], str]:
    clean = "".join(c for c in ciphertext.upper() if "A" <= c <= "Z")
    if not clean or n_cols <= 0:
        return (), ""

    num_rows = len(clean) // n_cols
    chunks = [clean[i * num_rows : (i + 1) * num_rows] for i in range(n_cols)]

    best_score = float("-inf")
    best_order = ()
    best_text = ""
    for perm in itertools.permutations(range(n_cols)):
        candidate = "".join(chunks[col][row] for row in range(num_rows) for col in perm)
        score = sum(BIGRAMS[(candidate[i], candidate[i + 1])]for i in range(len(candidate) - 1))

        if score > best_score:
            best_score = score
            best_order = perm
            best_text = candidate

    return best_order, best_text