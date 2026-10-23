import argparse
import math
import os
import re
import sys
from collections import Counter
from itertools import permutations

#SACADO DE WIKIPEDIA
ENGLISH_FREQS = {'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
    'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153,
    'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
    'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974,
    'Z': 0.00074}

#SACADO DE WIKIPEDIA
SPANISH_FREQS = {'A': 0.1253, 'B': 0.0142, 'C': 0.0468, 'D': 0.0586, 'E': 0.1368,
    'F': 0.0069, 'G': 0.0101, 'H': 0.0070, 'I': 0.0625, 'J': 0.0044,
    'K': 0.0002, 'L': 0.0497, 'M': 0.0315, 'N': 0.0671, 'O': 0.0868,
    'P': 0.0251, 'Q': 0.0088, 'R': 0.0687, 'S': 0.0798, 'T': 0.0463,
    'U': 0.0393, 'V': 0.0090, 'W': 0.0001, 'X': 0.0022, 'Y': 0.0090,
    'Z': 0.0052}

COMMON_BIGRAMS = {
    "TH",
    "HE",
    "IN",
    "ER",
    "AN",
    "RE",
    "ED",
    "ON",
    "ES",
    "ST",
    "EN",
    "AT",
    "TO",
    "NT",
    "HA",
    "ND",
    "OU",
    "EA",
    "NG",
    "AS",
    "OR",
    "TI",
    "IS",
    "ET",
    "IT",
    "AR",
    "TE",
    "SE",
    "HI",
    "OF",
}


# ==============================================================================
# 1. MÉTRICAS ESTADÍSTICAS (IC, CHI-CUADRADO Y N-GRAMAS)
# ==============================================================================
def clean_text(raw_text: str) -> str:
    return re.sub(r"[^A-Za-z]", "", raw_text).upper()


def calc_ic(text: str) -> float:
    n = len(text)
    if n <= 1:
        return 0.0
    counts = Counter(text)
    return sum(f * (f - 1) for f in counts.values()) / (n * (n - 1))


def unigram_chi_squared(text: str, target_freqs: dict) -> float:
    n = len(text)
    if n == 0:
        return float("inf")
    counts = Counter(text)
    chi2 = 0.0
    for char, expected_p in target_freqs.items():
        expected_count = expected_p * n
        observed_count = counts.get(char, 0)
        chi2 += ((observed_count - expected_count) ** 2) / expected_count
    return chi2


def score_bigrams(text: str) -> float:
    if len(text) < 2:
        return 0.0
    matches = sum(
        1 for i in range(len(text) - 1) if text[i : i + 2] in COMMON_BIGRAMS
    )
    return matches / (len(text) - 1)

def run_monoalphabetic_assistant(text: str, target_freqs: dict):
    n = len(text)
    counts = Counter(text)
    sorted_observed = sorted(
        counts.items(), key=lambda item: (-item[1], item[0])
    )
    sorted_expected = sorted(
        target_freqs.items(), key=lambda item: (-item[1], item[0])
    )

    print("\n" + "=" * 70)
    print("FREQUENCY ASSISTANT (Monoalphabetic Substitution Analysis)")
    print("=" * 70)
    print(f"{'Cipher Letter':<15}{'Count':<10}{'Observed %':<15}{'Expected'}")
    print("-" * 70)
    for i in range(min(15, len(sorted_observed))):
        c_letter, count = sorted_observed[i]
        pct = (count / n) * 100
        exp_letter, exp_val = (
            sorted_expected[i] if i < len(sorted_expected) else ("-", 0.0)
        )
        print(
            f"{c_letter:<15}{count:<10}{pct:>6.2f}%        {exp_letter} ({exp_val * 100:.1f}%)"
        )
    print(
        "\nManual substitution assistant ready: Frequency profile mapped to standard alphabet."
    )


def solve_vigenere_pipeline(ciphertext: str, target_freqs: dict):
    best_m = 1
    best_avg_ic = 0.0
    candidates = []

    for m in range(2, 17):
        cosets = [ciphertext[i::m] for i in range(m)]
        avg_ic = sum(calc_ic(c) for c in cosets) / m
        candidates.append((m, avg_ic))
        if avg_ic >= 0.055:
            best_m = m
            best_avg_ic = avg_ic
            break

    if best_m == 1:
        best_m, best_avg_ic = max(candidates, key=lambda x: x[1])

    print(
        f"  - Key length detection: Selected m = {best_m} (Coset Mean IC = {best_avg_ic:.4f})"
    )

    recovered_key = []
    for i in range(best_m):
        coset = ciphertext[i::best_m]
        best_shift = 0
        min_chi = float("inf")
        for shift in range(26):
            decrypted_coset = "".join(
                chr((ord(c) - 65 - shift) % 26 + 65) for c in coset
            )
            chi = unigram_chi_squared(decrypted_coset, target_freqs)
            if chi < min_chi:
                min_chi = chi
                best_shift = shift
        recovered_key.append(chr(best_shift + 65))

    key = "".join(recovered_key)
    plaintext = "".join(
        chr((ord(c) - 65 - (ord(key[i % len(key)]) - 65)) % 26 + 65)
        for i, c in enumerate(ciphertext)
    )
    return key, plaintext


def solve_columnar_pipeline(ciphertext: str, num_cols: int):
    n = len(ciphertext)
    num_rows = math.ceil(n / num_cols)
    best_score = -1.0
    best_pt = ""
    best_perm = None

    for perm in permutations(range(num_cols)):
        cols = [
            ciphertext[i * num_rows : (i + 1) * num_rows]
            for i in range(num_cols)
        ]
        grid = ["" for _ in range(num_rows)]
        for col_idx, orig_col in enumerate(perm):
            for row in range(len(cols[col_idx])):
                grid[row] += cols[col_idx][row]

        candidate_pt = "".join(grid)[:n]
        score = score_bigrams(candidate_pt)
        if score > best_score:
            best_score = score
            best_pt = candidate_pt
            best_perm = perm

    return best_perm, best_pt, best_score

def main():
    parser = argparse.ArgumentParser(
        description="Classical Cryptanalysis Routing Pipeline"
    )
    parser.add_argument(
        "--in",
        dest="input_file",
        required=True,
        help="Path to ciphertext file",
    )
    parser.add_argument(
        "--lang",
        choices=["en", "es"],
        default="en",
        help="Target language (default: en)",
    )
    parser.add_argument(
        "--cols",
        type=int,
        default=None,
        help="Number of columns for transposition (optional)",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        print(
            f"Error: Target file '{args.input_file}' not found.",
            file=sys.stderr,
        )
        sys.exit(1)

    with open(args.input_file, "r", encoding="utf-8") as f:
        raw_data = f.read()

    ciphertext = clean_text(raw_data)
    l_len = len(ciphertext)
    target_freqs = ENGLISH_FREQS if args.lang == "en" else SPANISH_FREQS

    print("\n" + "=" * 70)
    print("CRYPTANALYSIS PIPELINE AUDIT REPORT")
    print("=" * 70)
    print(
        f"Input file: {args.input_file} | Extracted length: L = {l_len} characters | Language: {args.lang.upper()}"
    )

    # 1. Medición del Índice de Coincidencia
    ic = calc_ic(ciphertext)
    chi2_raw = unigram_chi_squared(ciphertext, target_freqs)
    print(f"Index of Coincidence (IC): {ic:.4f} (Natural: ~0.0667, Random: ~0.0385)")
    print(f"Direct Unigram Chi-Square : {chi2_raw:.2f}")

    # 2. Enrutamiento y clasificación
    if ic < 0.055:
        # Polialfabético (Bajo IC)
        print("\nDecision: Polyalphabetic Substitution detected (IC < 0.055).")
        print(
            "Routing to Vigenère cryptanalysis engine (Kasiski / Coset IC matching)..."
        )
        key, plaintext = solve_vigenere_pipeline(ciphertext, target_freqs)
        print("\n[RESULT]")
        print(f"Recovered Key: {key}")
        print(f"Plaintext Preview: {plaintext[:120]}...")

    elif chi2_raw < 150.0:
        # Transposición (Alto IC + frecuencias unigramas conservadas del idioma)
        print(
            "\nDecision: Columnar Transposition detected (High IC + Direct English unigram correlation)."
        )
        if args.cols:
            candidate_cols = [args.cols]
            print(f"Using provided column count: n = {args.cols}")
        else:
            divisors = [d for d in range(2, 9) if l_len % d == 0]
            candidate_cols = divisors if divisors else list(range(2, 9))
            print(f"Candidate column counts evaluated: {candidate_cols}")

        best_overall_score = -1.0
        winner_pt = ""
        winner_cols = None
        winner_perm = None

        for n_col in candidate_cols:
            perm, pt, score = solve_columnar_pipeline(ciphertext, n_col)
            print(
                f"  - Columns n = {n_col} | Best bigram score = {score:.4f} | Permutation = {perm}"
            )
            if score > best_overall_score:
                best_overall_score = score
                winner_pt = pt
                winner_cols = n_col
                winner_perm = perm

        print("\n[RESULT]")
        print(
            f"Selected Columns: n = {winner_cols} (Permutation: {winner_perm})"
        )
        print(f"Plaintext Preview: {winner_pt[:120]}...")

    else:
        # Sustitución Monoalfabética (Alto IC + frecuencias alteradas respecto al alfabeto plano)
        print(
            "\nDecision: Monoalphabetic Substitution detected (High IC, but high unigram divergence)."
        )
        print(
            "Per assignment requirements, automatic solving is omitted; initiating frequency assistant."
        )
        run_monoalphabetic_assistant(ciphertext, target_freqs)

if __name__ == "__main__":
    main()