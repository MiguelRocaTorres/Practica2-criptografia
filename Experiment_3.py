import random
import string
import time
from break_columnar import attack as attack_columnar
from columnar import encrypt as columnar_encrypt
from reference import CORPUS

def get_clean_corpus() -> str:
    return "".join(c for c in CORPUS.upper() if "A" <= c <= "Z")


def get_random_sample(text: str, length: int) -> str:
    if len(text) <= length:
        text = text * ((length // len(text)) + 2)
    max_start = len(text) - length
    start = random.randint(0, max_start)
    return text[start : start + length]

def random_keyword(length: int) -> str:
    return "".join(random.sample(string.ascii_uppercase, length))

def run_columnar_experiments(column_counts, text_lengths, trials_per_cell=100) -> dict:
    corpus = get_clean_corpus()
    results = {c: {} for c in column_counts}
    total_cells = len(column_counts) * len(text_lengths)
    cell_idx = 0
    print(f"Starting Columnar Transposition evaluation ({trials_per_cell} trials/cell, {total_cells} total cells)...\n")
    for c in column_counts:
        for L in text_lengths:
            cell_idx += 1
            successes = 0
            t0 = time.time()
            for _ in range(trials_per_cell):
                plaintext = get_random_sample(corpus, L)
                key = random_keyword(c)
                ciphertext = columnar_encrypt(plaintext, key, pad="X")
                try:
                    res = attack_columnar(ciphertext, n_cols=c, language="en")
                except TypeError:
                    try:
                        res = attack_columnar(ciphertext, cols=c, language="en")
                    except TypeError:
                        res = attack_columnar(ciphertext, c)

                if isinstance(res, tuple):
                    recovered_pt = res[1]
                else:
                    recovered_pt = res

                if recovered_pt[:L].upper() == plaintext.upper():
                    successes += 1

            accuracy = successes / trials_per_cell
            elapsed = time.time() - t0
            results[c][L] = accuracy

            print(f"[{cell_idx}/{total_cells}] Columns = {c}, Length = {L} -> Accuracy: {accuracy:.1%} ({elapsed:.2f}s)")

    return results

def print_markdown_table(results: dict, text_lengths: list[int]):
    headers = ["Columns (C)"] + [f"L = {L}" for L in text_lengths]
    print("| " + " | ".join(headers) + " |")
    for c, row in results.items():
        cols = [f"{c}"] + [f"{row[L]:.1%}" for L in text_lengths]
        print("| " + " | ".join(cols) + " |")

def main():
    columns = [4, 5, 6, 7]
    lengths = [60, 120, 200]
    trials = 100

    results = run_columnar_experiments(columns, lengths, trials_per_cell=trials)
    print_markdown_table(results, lengths)

if __name__ == "__main__":
    main()