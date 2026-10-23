import random
import string
from columnar import encrypt as columnar_encrypt
from measure import classify
from P1.monoalpha import encrypt as mono_encrypt
from reference import CORPUS

ENGLISH_FREQS = {
    "A": 0.08167, "B": 0.01492, "C": 0.02782, "D": 0.04253, "E": 0.12702,
    "F": 0.02228, "G": 0.02015, "H": 0.06094, "I": 0.06966, "J": 0.00153,
    "K": 0.00772, "L": 0.04025, "M": 0.02406, "N": 0.06749, "O": 0.07507,
    "P": 0.01929, "Q": 0.00095, "R": 0.05987, "S": 0.06327, "T": 0.09056,
    "U": 0.02758, "V": 0.00978, "W": 0.02360, "X": 0.00150, "Y": 0.01974,
    "Z": 0.00074}
POPULATION = list(ENGLISH_FREQS.keys())
WEIGHTS = list(ENGLISH_FREQS.values())

def get_clean_text() -> str:
    return "".join(c for c in CORPUS.upper() if "A" <= c <= "Z")

def get_random_sample(text: str, length: int) -> str:
    max_start = len(text) - length
    start = random.randint(0, max_start)
    return text[start : start + length]

def random_monoalpha_key() -> str:
    chars = list(string.ascii_uppercase)
    random.shuffle(chars)
    return "".join(chars)

def random_columnar_key() -> str:
    k_len = random.randint(3, 8)
    return "".join(random.choices(string.ascii_uppercase, k=k_len))

def run_experiment(lengths, n_samples=150, pad_mode="constant"):
    reference = get_clean_text()
    results = {}
    for L in lengths:
        col_errors = 0
        mono_errors = 0
        for _ in range(n_samples):
            plain_col = get_random_sample(reference, L)
            col_key = random_columnar_key()
            pad_char = (
                "X"
                if pad_mode == "constant"
                else random.choices(POPULATION, weights=WEIGHTS)[0])

            c_col = columnar_encrypt(plain_col, col_key, pad=pad_char)
            pred_col = classify(c_col, language="en")
            if pred_col != "transposition":
                col_errors += 1

            plain_mono = get_random_sample(reference, L)
            mono_key = random_monoalpha_key()
            c_mono = mono_encrypt(plain_mono, mono_key)
            pred_mono = classify(c_mono, language="en")
            if pred_mono != "substitution":
                mono_errors += 1

        results[L] = {
            "trans_err": col_errors / n_samples,
            "mono_err": mono_errors / n_samples,
            "total_err": (col_errors + mono_errors) / (2 * n_samples)}

    return results

def main():
    lengths = [60, 120, 250, 400]
    n_samples = 150
    res_x = run_experiment(lengths, n_samples, pad_mode="constant")
    res_dist = run_experiment(lengths, n_samples, pad_mode="distribution")
    header = ("| Len | Transp Er | Mono Er | Total Er | Transp Er | Mono Er | Total Er |\n")
    rows = []
    for L in lengths:
        row = (
            f"| {L} | {res_x[L]['trans_err']:.2%} | {res_x[L]['mono_err']:.2%} | {res_x[L]['total_err']:.2%} | "
            f"{res_dist[L]['trans_err']:.2%} | {res_dist[L]['mono_err']:.2%} | {res_dist[L]['total_err']:.2%} |"
        )
        rows.append(row)

    print(header + "\n".join(rows))

if __name__ == "__main__":
    main()