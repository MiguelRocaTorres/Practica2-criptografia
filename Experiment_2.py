import random
import string
from break_vigenere import attack as attack_vigenere
from keylength import find_key_length
from reference import CORPUS
try:
    from P1.vigenere import encrypt as vigenere_encrypt
except ImportError:
    def vigenere_encrypt(plaintext: str, key: str) -> str:
        key = key.upper()
        clean = "".join(c for c in plaintext.upper() if "A" <= c <= "Z")
        res = []
        for i, c in enumerate(clean):
            shift = ord(key[i % len(key)]) - ord("A")
            res.append(chr((ord(c) - ord("A") + shift) % 26 + ord("A")))
        return "".join(res)

def get_clean_corpus() -> str:
    return "".join(c for c in CORPUS.upper() if "A" <= c <= "Z")

def get_random_sample(text: str, length: int) -> str:
    if len(text) <= length:
        text = text * ((length // len(text)) + 2)
    max_start = len(text) - length
    start = random.randint(0, max_start)
    return text[start : start + length]

def random_key(length: int) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=length))

def run_vigenere_experiments(key_lengths, text_lengths, trials_per_cell=100) -> tuple[dict, dict]:
    corpus = get_clean_corpus()
    complete_key_results = {m: {} for m in key_lengths}
    key_length_results = {m: {} for m in key_lengths}
    total_cells = len(key_lengths) * len(text_lengths)
    current_cell = 0
    print(f"Starting evaluation ({trials_per_cell} trials/cell, {total_cells} total cells)...\n")
    for m in key_lengths:
        for L in text_lengths:
            current_cell += 1
            key_len_correct = 0
            full_key_correct = 0
            for _ in range(trials_per_cell):
                plaintext = get_random_sample(corpus, L)
                true_key = random_key(m)
                ciphertext = vigenere_encrypt(plaintext, true_key)
                try:
                    pred_m = find_key_length(ciphertext)
                except Exception:
                    pred_m = None

                try:
                    rec_key, _ = attack_vigenere(ciphertext, language="en")
                except TypeError:
                    rec_key, _ = attack_vigenere(ciphertext)
                except Exception:
                    rec_key = ""

                if pred_m is None and rec_key:
                    pred_m = len(rec_key)

                if pred_m == m:
                    key_len_correct += 1

                if rec_key.upper() == true_key.upper():
                    full_key_correct += 1

            p_full = full_key_correct / trials_per_cell
            p_len = key_len_correct / trials_per_cell
            complete_key_results[m][L] = p_full
            key_length_results[m][L] = p_len
            print(f"[{current_cell}/{total_cells}] Key len m={m}, Text len L={L} -> Length Acc: {p_len:.1%}, Complete Key: {p_full:.1%}")

    return complete_key_results, key_length_results

def print_markdown_table(title: str, results: dict, text_lengths: list[int]):
    print(f"\n### {title}\n")
    headers = ["Key Length (m)"] + [f"L = {L}" for L in text_lengths]
    print("| " + " | ".join(headers) + " |")
    for m, row in results.items():
        cols = [f"{m}"] + [f"{row[L]:.1%}" for L in text_lengths]
        print("| " + " | ".join(cols) + " |")

def main():
    key_lengths = [3, 5, 7, 9]
    text_lengths = [100, 150, 200, 300, 400]
    trials = 100
    full_res, len_res = run_vigenere_experiments(key_lengths, text_lengths, trials_per_cell=trials)
    print_markdown_table("Table 1: Complete Key Recovery Rate", full_res, text_lengths)
    print_markdown_table("Table 2: Key Length Accuracy Rate Alone", len_res, text_lengths)

if __name__ == "__main__":
    main()