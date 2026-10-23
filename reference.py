CORPUS = """
Cryptanalysis of the polyalphabetic Vigenere cipher historically represented a major 
turning point in the history of cryptography. For centuries, the cipher was regarded 
as le chiffre indechiffrable because the shifting alphabets smoothed out the distinctive 
spikes and troughs of natural language unigram frequencies. In eighteen sixty-three, 
Friedrich Kasiski published the first general method for breaking polyalphabetic ciphers, 
relying on the observation that identical segments of plaintext encrypted with the same 
portion of the key produce identical segments of ciphertext. By calculating the greatest 
common divisor of the distances between these repeated sequences, an analyst can determine 
the length of the keyword. Later, William Frederick Friedman introduced the index of 
coincidence, providing a rigorous statistical measure that quantifies the non-uniformity 
of letter distributions. Once the key length m is correctly established, the ciphertext 
can be decomposed into m independent cosets, each representing a monoalphabetic Caesar 
shift cipher. Each coset is then independently solved by comparing its letter frequency 
distribution against standard English frequencies using the chi-square statistic or 
dot-product maximization. However, when the ciphertext length is small relative to the 
period, each individual coset contains very few characters, drastically increasing sampling 
variance and making both key length determination and individual shift recovery error-prone. 
As the volume of intercept increases, empirical frequencies stabilize rapidly around their 
expected theoretical values, enabling reliable and fully automated cryptanalysis.
"""