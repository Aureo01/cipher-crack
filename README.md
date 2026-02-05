# cipher-crack
Cipher_crack is a lightweight and practical tool designed to detect and automatically try multiple decryption/obfuscation techniques on a given text.

It’s built for CTFs, quick analysis, pentesting, light reversing, or curiosity-driven hacking, without heavy dependencies or unnecessary resource usage.
Works smoothly even on low-RAM devices, small VPSs, or minimal Linux setups.

---

# What does it do?

Analyzes the input text

Attempts to identify the cipher type

Tries multiple decoding/decryption methods

Displays the results in a clean, readable comparison table

No guessing. No black magic.
You see everything it finds, and you decide what makes sense.

---

# Supported methods

Caesar cipher (all shifts)

- ROT13

- Base64

- Vigenère (common keys)

- XOR (simple keys)

- Plain / readable text detection

- Perfect for spotting weak or classic obfuscation techniques fast.

---

# Usage 

**Try all methods automatically**

- python3 crypto_suite.py "SGVsbG8gV29ybGQ="

**Decode Base64 specifically**

- python3 crypto_suite.py "SGVsbG8=" --method base64

**Decode ROT13**

- python3 crypto_suite.py "Uryyb Jbeyq" --method rot13

**Decode Caesar (will try all shifts)**

- python3 crypto_suite.py "Khoor Zruog" --method caesar

**Decode Vigenère**

- python3 crypto_suite.py "Rijvs Asvph" --method vigenere

---

# Design philosophy

-Fast

-Lightweight

-Practical

-No assumptions

Built to give you answers quickly, not overwhelm you with frameworks.

**Disclaimer**
cipher_crack does not aim to break strong cryptography.
It focuses on classic ciphers, weak implementations, and common obfuscation techniques—exactly what you’ll find in CTFs and real-world apps more often than people admit

