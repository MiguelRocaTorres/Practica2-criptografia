def key_order(keyword: str) -> list[int]:
    order = [0] * len(keyword)
    sorted_indices = sorted(range(len(keyword)), key = lambda i: keyword[i])
    for rank, idx in enumerate(sorted_indices, 1):
        order[idx] = rank

    return order

def encrypt(plaintext: str, keyword: str, pad: str = "X") -> str:
    k = len(keyword)
    needed = (k -len(plaintext) % k) % k
    plaintext += (pad * needed)[:needed]
    order = key_order(keyword)
    sorted_cols = sorted(range(k), key = lambda i: order[i])
    cols = [plaintext[i::k] for i in range(k)]
    return "".join(cols[i] for i in sorted_cols)

def decrypt(ciphertext: str, keyword: str) -> str:
    k = len(keyword)
    num_rows = len(ciphertext) // k
    order = key_order(keyword)
    sorted_cols = sorted(range(k), key = lambda i: order[i])
    cols = [""] * k
    for j, col_idx in enumerate(sorted_cols):
        cols[col_idx] = ciphertext[j * num_rows: (j + 1) * num_rows]

    plaintext = []
    for r in range(num_rows):
        for c in range(k):
            plaintext.append(cols[c][r])

    return "".join(plaintext)

print(key_order("ENIGMA"))
print(key_order("ROTOR"))
print(key_order("KASISKI"))
print(key_order("BLETCHLEY"), "\n")
print(encrypt("MYSECRETMESSAGE", "CIPHER"))
print(decrypt("MEACSXEEXYTGSMERSX", "CIPHER"))
print(encrypt("THE INDEX OF COINCIDENCE", "KASISKI"))

def encrypt_double(plaintext: str, kw1: str, kw2: str, pad: str = "X") -> str:
    return encrypt(encrypt(plaintext, kw1, pad = pad), kw2, pad = pad)

def decrypt_double(ciphertext: str, kw1 : str, kw2: str) -> str:
    inter = decrypt(ciphertext, kw2)
    pad_len = len(inter) % len(kw1)
    if pad_len > 0:
        inter = inter[:-pad_len]

    return decrypt(inter, kw1)

print()
print(encrypt_double("THESAMEKEYMUSTNEVERBEUSEDTWICE", "ROTOR", "ENIGMA"))
print(decrypt_double("WCTEIHSTAEVREBEUTMNSUEEDSEEMYK", "ROTOR", "ENIGMA"))