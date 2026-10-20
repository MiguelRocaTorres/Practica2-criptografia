def encrypt(plaintext: str, rails: int) -> str:
    fence = [[] for _ in range(rails)]
    rail = 0
    step = 1
    for char in plaintext:
        fence[rail].append(char)
        if rail == 0:
            step = 1
        elif rail == rails - 1:
            step = -1

        rail += step

    return "".join("".join(row) for row in fence)

def decrypt(ciphertext: str, rails: int) -> str:
    pattern = []
    rail = 0
    step = 1
    for _ in range(len(ciphertext)):
        pattern.append(rail)
        if rail == 0:
            step = 1
        elif rail == rails - 1:
            step = -1

        rail += step

    positions = sorted(range(len(ciphertext)), key = lambda i: pattern[i])
    plaintext = [""] * len(ciphertext)
    for char, pos in zip(ciphertext, positions):
        plaintext[pos] = char

    return "".join(plaintext)

print(encrypt("MYSECRETMESSAGE", 2))
print(encrypt("MYSECRETMESSAGE", 3))
print(encrypt("MYSECRETMESSAGE", 4))
print(decrypt(encrypt("MYSECRETMESSAGE", 5), 5))