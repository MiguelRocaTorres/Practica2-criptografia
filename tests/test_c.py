import random
import string
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from break_columnar import attack as attack_columnar
from break_vigenere import attack as attack_vigenere
from columnar import encrypt as columnar_encrypt
from reference import CORPUS

def clean_text(text: str) -> str:
    return "".join(c for c in text.upper() if "A" <= c <= "Z")

def vigenere_encrypt(plaintext: str, key: str) -> str:
    clean = clean_text(plaintext)
    key = key.upper()
    return "".join(chr((ord(c) - ord("A") + ord(key[i % len(key)]) - ord("A")) % 26 + ord("A")) for i, c in enumerate(clean))

def get_random_sample(text: str, length: int) -> str:
    if len(text) <= length:
        text = text * ((length // len(text)) + 2)
    start = random.randint(0, len(text) - length)
    return text[start : start + length]

def test_vigenere_attack_recovery():
    corpus = clean_text(CORPUS)
    text_len = 400
    key_len = 3
    trials = 20
    successes = 0

    for i in range(trials):
        sample = get_random_sample(corpus, text_len)
        true_key = "".join(random.choices(string.ascii_uppercase, k=key_len))
        ciphertext = vigenere_encrypt(sample, true_key)

        try:
            res = attack_vigenere(ciphertext, language="en")
        except TypeError:
            res = attack_vigenere(ciphertext)

        recovered_key = res[0] if isinstance(res, tuple) else res
        print(f"\n[Ensayo {i+1:02d}] Clave real: {true_key} | Obtenida: {recovered_key}")

        if str(recovered_key).upper() == true_key.upper():
            successes += 1

    assert (
        successes >= 18
    ), f"Vigenere key recovery below acceptable threshold: {successes}/{trials}"

def test_columnar_attack_recovery():
    corpus = clean_text(CORPUS)
    text_len = 200
    cols = 4
    trials = 20
    successes = 0
    for _ in range(trials):
        sample = get_random_sample(corpus, text_len)
        key = "".join(random.sample(string.ascii_uppercase, cols))
        ciphertext = columnar_encrypt(sample, key, pad="X")
        try:
            res = attack_columnar(ciphertext, n_cols=cols, language="en")
        except TypeError:
            try:
                res = attack_columnar(ciphertext, cols=cols, language="en")
            except TypeError:
                res = attack_columnar(ciphertext, cols)

        recovered_pt = res[1] if isinstance(res, tuple) else res
        if recovered_pt[:text_len].upper() == sample.upper():
            successes += 1

    assert successes >= 19, (f"Columnar transposition attack below acceptable threshold: {successes}/{trials}")