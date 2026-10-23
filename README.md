# Laboratory Practice 2: Classical Cryptanalysis and Transposition Ciphers

---

## 1. How to Run Everything

All scripts and tests must be executed from the project root directory.

### Environment & Dependencies

The test suite runs on `pytest`:

```bash
python -m pip install pytest
```

### Running the Test Suite

Execute the complete test suite:

```bash
python -m pytest -v
```

Execution output:

<img width="1580" height="226" alt="Captura de pantalla 2026-10-23 152849" src="https://github.com/user-attachments/assets/0b9961e2-f9f4-4a64-8f9f-81f801258f90" />

Individual test files can be executed separately:

```bash
python -m pytest tests/test_b1.py -v
python -m pytest tests/test_b3.py -v
python -m pytest tests/test_c.py -v
```

### Running the Empirical Experiments

Generate the empirical benchmark tables:

```bash
# Experiment 1: Cipher family classifier (IC-based)
python Experiment_1.py

# Experiment 2: Vigenère attack performance across lengths and key sizes
python Experiment_2.py

# Experiment 3: Columnar transposition attack across lengths and column counts
python Experiment_3.py
```

---

## 2. A3: Padding and Double Transposition

In columnar transposition ciphers, if the plaintext length `L` is not an exact multiple of the key length `W = len(k)`, the final row of the grid is incomplete. The encryption routine fills these empty cells using a padding character (by default, `'X'`).

When applying double transposition (`C = E_k2(E_k1(M))`):

1. **Grid Formation and Incomplete Blocks:** The first transposition grid has dimensions `ceil(L / W_1) x W_1`. The ciphertext output `C_1` has length `L' = ceil(L / W_1) * W_1`, which incorporates the initial padding.
2. **Second Encryption Layer:** The second transposition treats `C_1` as its input plaintext. If `L'` is not divisible by `W_2 = len(k_2)`, a second layer of padding is added, expanding the length to `L'' = ceil(L' / W_2) * W_2`.
3. **Decryption Requirements:** Decryption must strictly apply the inverse operations in reverse order: `M = D_k1(D_k2(C))`. For this round-trip to succeed deterministically when `L` is not a multiple of either key length, the decryption routines must compute the exact rectangular matrix dimensions using the known padded lengths (`L''` and `L'`). Intermediate padding characters introduced during `E_k1` must not be stripped prior to executing `D_k1`; doing so alters the string length and breaks the coordinate mapping of the inner grid. Padding may only be removed once the final plaintext grid has been read out.

---

## 3. B1: Minimum Trustworthy Length for Index of Coincidence

The unigram Index of Coincidence (`IC`) measures the probability that two randomly selected letters from a ciphertext are identical:

`IC = sum(f_i * (f_i - 1)) / (N * (N - 1))`

For natural English text, the theoretical expectation is `kappa_p ≈ 0.0667`, while for an alphabet with a uniform distribution (ideal random sequence or polyalphabetic ciphertext with large period) it is `kappa_r ≈ 0.0385`.

The sampling variance of the `IC` statistic scales inversely with sample size: `Var(IC) ∝ O(1/N)`.

- **When N < 50:** Statistical fluctuations dominate: the `IC` of genuine English text can easily dip below 0.050, while accidental repeats in short polyalphabetic samples can push the empirical value above 0.055.
- **As N reaches 100 letters:** The sample variance decreases sufficiently such that the distributions of monoalphabetic and polyalphabetic texts exhibit a clean separation (>= 3 standard deviations). `N = 100` characters is the empirical minimum length for reliable automated classification without significant false-positive rates.

---

## 4. B2: Cipher Family Classifier

### Selected Threshold

- **Chosen Threshold:** `T = 0.055`
- **Selection Rationale:** The midpoint between natural English (`≈ 0.0667`) and uniform noise (`≈ 0.0385`) is approximately 0.0526. Selecting `T = 0.055` provides a conservative buffer against short-text sample variance, preventing polyalphabetic cosets with accidental clusters from being misclassified as monoalphabetic while remaining lenient enough to absorb negative variance dips in English plaintexts down to `N ≈ 75`.

### Measurement Tables

#### Error Rate (%) by Ciphertext Length

<img width="649" height="103" alt="Captura de pantalla 2026-10-23 153327" src="https://github.com/user-attachments/assets/105667c7-858b-43ee-9778-4dfebbf61bbb" />

> **Note on columns:** The first three metric columns correspond to the initial baseline classifier, whereas the last three columns reflect the improved classifier (incorporating refined thresholding / n-gram statistics), which achieves 0.00% error starting from `N >= 250`.

### Answers to the Four B2 Questions

1. **Why does a transposition cipher have the same IC as natural English?**  
   Transposition ciphers only permute character positions without altering character identities. Because the global letter frequency counts `{f_A, f_B, ..., f_Z}` remain unchanged, the numerator `sum(f_i * (f_i - 1))` is identical to that of the plaintext.

2. **Why does a monoalphabetic substitution cipher maintain the English IC?**  
   Monoalphabetic substitution applies a bijective mapping (permutation of the alphabet). This renames the counts `{f_i}` but preserves the overall multiset of frequencies. Summing over all letters yields the exact same total sum of squares.

3. **Why does a polyalphabetic cipher reduce the IC toward the uniform distribution?**  
   A polyalphabetic cipher with period `m` encrypts text using `m` distinct Caesar shifts. When analyzing the aggregate ciphertext as a single stream, the character frequencies represent a mixture of shifted distributions, evening out peaks and troughs toward a uniform distribution (`kappa_r ≈ 0.0385`).

4. **How does text length influence classification confidence?**  
   At small lengths (`N <= 50`), sampling variance is large, causing occasional misclassifications. As `N` increases (`N >= 100`), empirical frequencies rapidly converge to their population expectations by the Law of Large Numbers, driving classification accuracy to 100%.

---

## 5. B3: Kasiski Examination and the GCD Fallacy

The Kasiski examination locates repeated substrings of length `>= 3` and records the distances between their occurrences.

- **The GCD Silent Failure Condition:** If an analyst simply takes the greatest common divisor (`gcd`) of all identified interval distances:  
  `gcd(d_1, d_2, ..., d_k)`  
  the method will silently collapse to 1 whenever a single accidental repeat occurs. Accidental repeats arise from common English digrams or trigrams that happen to be encrypted at locations not separated by a multiple of the key length. If 15 intervals are exact multiples of 5, but one random coincidence produces a distance of 21, then:  
  `gcd(15, 35, 50, ..., 21) = 1`

- **Why `factor_tally` is Superior:** Instead of enforcing strict divisibility across all distances, `factor_tally` tallies the divisors of each distance independently. This acts as a statistical voting filter: true key lengths consistently appear as factors across all legitimate structural repeats, achieving a high tally count that easily dominates the sporadic background noise of accidental coincidences.

---

## 6. C1: Coset Index of Coincidence Table

A polyalphabetic ciphertext encrypted with key length `m* = 3` is partitioned into `m` candidate cosets for `m` in `[1, 16]`. The average `IC` across all cosets is computed:

<img width="535" height="338" alt="Captura de pantalla 2026-10-23 155852" src="https://github.com/user-attachments/assets/c3e29665-03b0-4f02-ae22-e91d6908529e" />

- **Analysis:** The fundamental key length `m = 3` produces an immediate jump in the mean IC to `0.0634`, aligning with standard English expectation. Every integer multiple of the true period (`m = 6, 9, 12, 15`) also maintains high IC values (`> 0.061`) because their slices preserve monoalphabetic properties. All non-multiples mix distinct Caesar shifts and remain bounded within the polyalphabetic background baseline (`~0.042 - 0.045`).

---

## 7. C2: Vigenère Attack Evaluation

### Table 1: Complete Key Recovery Rate (100 trials/cell)

<img width="633" height="144" alt="Captura de pantalla 2026-10-23 154409" src="https://github.com/user-attachments/assets/79fa2839-137d-447b-8d13-8035657a3346" />

### Table 2: Key Length Accuracy Rate Alone (100 trials/cell)

<img width="616" height="142" alt="Captura de pantalla 2026-10-23 154609" src="https://github.com/user-attachments/assets/e539a030-0720-4434-9b45-1228bc3870e7" />

### Answers to the Three C2 Questions

1. **How does the ratio `L/m` govern cryptanalytic success?**  
   The critical bottleneck is the effective slice length `L/m` allocated to each independent coset. When `L/m < 20` (e.g., `m = 7` at `L = 100`, where `L/m ≈ 14`), unigram frequency distributions deviate significantly from standard English expectations due to high sample variance, causing complete key recovery to drop to 5.0%. Once `L/m >= 50` to `60` letters per coset, unigram frequencies stabilize and allow independent Caesar decryptions to cross the 90%+ recovery threshold.

2. **Why do longer keys require proportionally longer ciphertexts?**  
   Because the ciphertext is split across `m` separate cosets, each additional key character increases the dispersion of data. To maintain an identical level of statistical certainty in each coset's frequency counts, the total intercept length `L` must grow linearly with key length `m`. As shown in Table 1, achieving ~70% recovery requires only `L = 150` for `m = 5`, but demands `L = 300` for `m = 7` and `L = 400` for `m = 9`.

3. **What happens if key length detection makes an error?**  
   * **Underestimating `m` (selecting a proper divisor):** Each extracted coset contains characters encrypted under multiple distinct Caesar shifts. The resulting unigram distribution remains flattened and polyalphabetic, causing frequency matching to fail completely.
   * **Overestimating `m` (selecting a multiple `k * m`):** Each coset remains strictly monoalphabetic (since every `k * m`-th character shares the same underlying shift). The attack deduces the true key repeated `k` times (e.g., recovering `ABCABC` instead of `ABC`), which still decrypts the message into readable plaintext.

---

## 8. C3: Columnar Transposition Attack and Workable `n`

### Table 1: Plaintext Recovery Success Rate (%) Across 100 Trials

<img width="379" height="105" alt="Captura de pantalla 2026-10-23 160942" src="https://github.com/user-attachments/assets/88f2de50-d36f-46f7-80f8-83a822e31b9a" />

### Benchmark Execution Log (Accuracy and Runtime per Configuration)

<img width="671" height="277" alt="Captura de pantalla 2026-10-23 160943" src="https://github.com/user-attachments/assets/518ef548-4e1b-454d-b7f8-b17619ac89ab" />

- **One-Sentence Question:** The attack recovers the column permutation by maximizing the cumulative log-probability of adjacent bigrams and trigrams formed when candidate columns are placed side-by-side, as correct permutations assemble natural English words while incorrect ones generate statistically improbable consonant clusters.
- **Largest Workable `n`:** The largest workable key length under exhaustive permutation search is `n = 8` columns. Exhaustive evaluation of `8! = 40,320` permutations executes in approximately 1 to 2 seconds. For `n = 9` (`362,880` permutations), runtime increases to several tens of seconds, and for `n >= 10` (`3,628,800` permutations), brute force becomes computationally impractical without heuristic search methods (such as hill climbing or genetic algorithms).

---

## 9. Part D Pipeline Analysis

The Part D routing pipeline makes an initial routing decision based exclusively on the unigram Index of Coincidence. The fundamental cryptographic property that makes this possible is the invariance of single-letter marginal probabilities under character rearrangement and monoalphabetic substitution: neither classical transposition nor Caesar/monoalphabetic substitution modifies the unigram probability distribution. 

A cipher that completely defeats this classification pipeline is homophonic substitution (or a balanced polygraphic cipher such as Playfair). By mapping frequent plaintext letters to multiple distinct ciphertext symbols proportional to their frequency, homophonic substitution flattens letter frequencies to a near-uniform distribution (`IC ≈ 0.0385`). Consequently, the pipeline misidentifies the ciphertext as polyalphabetic and routes it to the Vigenère solver, failing to attempt monoalphabetic or transposition cryptanalysis.

---

## 10. Anything That Does Not Work, Stated Plainly

1. **Short Ciphertexts (`L < 50`):** In very short texts, sampling variance causes the Index of Coincidence to fluctuate widely. Polyalphabetic ciphers with short keys can produce `IC > 0.055`, causing false positives in the B2 classifier.
2. **Exhaustive Columnar Transposition for `n > 8`:** The columnar cryptanalysis module relies on testing all `n!` permutations. It is strictly limited to `n <= 8`; attempting to crack keys with `n >= 10` columns without heuristic optimization causes excessive execution times or process timeouts.
3. **Padding Distortion on Short Text Bigram Scoring:** When a columnar ciphertext contains significant `'X'` padding at the end of several columns, bigram frequency scoring near the final grid rows is degraded, occasionally causing near-tie scores with suboptimal column orderings in texts under 80 characters.
