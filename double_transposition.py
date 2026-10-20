from columnar import encrypt, decrypt

def encrypt_double(plaintext: str, kw1: str, kw2: str, pad: str = "X") -> str:
    return encrypt(encrypt(plaintext, kw1, pad = pad), kw2, pad = pad)

def decrypt_double(ciphertext: str, kw1 : str, kw2: str) -> str:
    inter = decrypt(ciphertext, kw2)
    pad_len = len(inter) % len(kw1)
    if pad_len > 0:
        inter = inter[:-pad_len]

    return decrypt(inter, kw1)

print(encrypt_double("THESAMEKEYMUSTNEVERBEUSEDTWICE", "ROTOR", "ENIGMA"))
print(decrypt_double("WCTEIHSTAEVREBEUTMNSUEEDSEEMYK", "ROTOR", "ENIGMA"))