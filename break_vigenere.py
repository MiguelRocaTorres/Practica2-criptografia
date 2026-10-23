from keylength import find_key_length
from P1.break_caesar import break_caesar

def clean(text: str) -> str:
    return "".join(c for c in text.upper() if "A" <= c <= "Z")

def attack(ciphertext: str, language: str = "en") -> tuple[str, str]:
    text = clean(ciphertext)
    m = find_key_length(text)
    key_chars = []
    for i in range(m):
        coset = text[i::m]
        shift = break_caesar(coset)
        key_chars.append(chr(ord("A") + shift))

    key = "".join(key_chars)
    plaintext = []
    for idx, c in enumerate(text):
        shift = ord(key[idx % m] - ord("A"))
        plaintext.append(chr((ord(c) - ord("A") - shift) % 26 + ord("A")))

    return key, "".join(plaintext)