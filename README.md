# 🔐 Classical Cryptography Toolkit

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Security](https://img.shields.io/badge/Security-Cryptography-red?style=for-the-badge&logo=security&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

**A comprehensive Python implementation of classical encryption ciphers and cryptanalysis tools**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Examples](#-examples) • [Documentation](#-documentation)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Supported Ciphers](#-supported-ciphers)
- [Installation](#-installation)
- [Usage](#-usage)
  - [Encryption](#encryption)
  - [Decryption](#decryption)
  - [Cryptanalysis](#cryptanalysis)
- [Examples](#-examples)
- [Technical Details](#-technical-details)
- [Project Structure](#-project-structure)
- [Academic Context](#-academic-context)
- [Security Notice](#-security-notice)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 🎯 Overview

This project demonstrates both the **implementation** of historical cryptographic algorithms and the **techniques used to break them**. It serves as an educational tool for understanding:

- How classical encryption schemes work
- Why simple substitution ciphers are insecure
- Modern cryptanalysis techniques
- The importance of key space and randomness

**Perfect for:** Security students, cryptography enthusiasts, and anyone learning about information security fundamentals.

---

## ✨ Features

### 🔒 Cipher Implementations
- ✅ **Caesar Cipher** - Classic shift-based substitution
- ✅ **Affine Cipher** - Mathematical substitution using modular arithmetic
- ✅ **Monoalphabetic Substitution** - Custom alphabet mapping

### 🔓 Cryptanalysis Tools
- ✅ **Brute Force Attack** - Exhaustive key search for Caesar and Affine ciphers
- ✅ **Frequency Analysis** - Statistical attack on monoalphabetic ciphers
- ✅ **Dictionary Validation** - Automated plaintext verification
- ✅ **Performance Optimized** - Efficient algorithms for rapid analysis

### 💻 Additional Features
- ✅ Command-line interface with `argparse`
- ✅ Support for both encryption and decryption
- ✅ Comprehensive error handling
- ✅ Pure Python implementation (no external crypto libraries)
- ✅ Detailed logging of cryptanalysis results

---

## 🔐 Supported Ciphers

### 1. Caesar Cipher

**Algorithm:** `E(x) = (x + k) mod 26`

- **Key Space:** 25 possible keys
- **Strength:** Trivially breakable with brute force
- **Attack Time:** < 1 second

### 2. Affine Cipher

**Algorithm:** `E(x) = (ax + b) mod 26`

- **Requirements:** `gcd(a, 26) = 1` (a must be coprime with 26)
- **Key Space:** 12 × 26 = 312 possible keys
- **Strength:** Weak, vulnerable to frequency analysis
- **Attack Time:** < 2 seconds

### 3. Monoalphabetic Substitution Cipher

**Algorithm:** Direct letter-to-letter substitution with custom alphabet

- **Key Space:** 26! ≈ 4 × 10²⁶ possible keys
- **Strength:** Moderate, but vulnerable to frequency analysis
- **Attack Time:** 5-30 seconds (depending on text length)

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- No external dependencies required (uses only Python standard library)

### Clone the Repository

```bash
git clone https://github.com/memo-13-byte/Classical-Cryptography-Toolkit.git
cd Classical-Cryptography-Toolkit
```

### Verify Installation

```bash
python ciphers.py --help
python break.py --help
```

---

## 💡 Usage

### Encryption

#### Caesar Cipher
```bash
python ciphers.py caesar plaintext.txt e -s 13
```

**Parameters:**
- `caesar` - Cipher type
- `plaintext.txt` - Input file
- `e` - Encrypt mode
- `-s 13` - Shift value (0-25)

#### Affine Cipher
```bash
python ciphers.py affine plaintext.txt e -a 5 -b 8
```

**Parameters:**
- `affine` - Cipher type
- `-a 5` - Multiplicative key (must be coprime with 26)
- `-b 8` - Additive key (shift value)

#### Monoalphabetic Cipher
```bash
python ciphers.py mono plaintext.txt e -k QWERTYUIOPASDFGHJKLZXCVBNM
```

**Parameters:**
- `mono` - Cipher type
- `-k` - Substitution alphabet (26 unique letters)

### Decryption

```bash
# Caesar
python ciphers.py caesar ciphertext.txt d -s 13

# Affine
python ciphers.py affine ciphertext.txt d -a 5 -b 8

# Monoalphabetic
python ciphers.py mono ciphertext.txt d -k QWERTYUIOPASDFGHJKLZXCVBNM
```

### Cryptanalysis

Break encrypted messages automatically:

```bash
# Break Caesar Cipher
python break.py caesar encrypted.txt

# Break Affine Cipher
python break.py affine encrypted.txt

# Break Monoalphabetic Cipher (using frequency analysis)
python break.py mono encrypted.txt
```

**Output:** Successfully decrypted text saved to `break_[cipher].txt`

---

## 📚 Examples

### Example 1: Caesar Cipher

```bash
# Create plaintext file
echo "HELLO WORLD" > message.txt

# Encrypt with shift 3
python ciphers.py caesar message.txt e -s 3
# Output: KHOOR ZRUOG

# Decrypt
python ciphers.py caesar cipher_caesar.txt d -s 3
# Output: HELLO WORLD

# Break (without knowing the key)
python break.py caesar cipher_caesar.txt
# Automatically finds shift=3 and outputs: HELLO WORLD
```

### Example 2: Affine Cipher

```bash
# Encrypt
python ciphers.py affine secret.txt e -a 5 -b 8
# Uses formula: E(x) = (5x + 8) mod 26

# Break with cryptanalysis
python break.py affine cipher_affine.txt
# Tests all 312 valid (a,b) combinations
# Outputs decrypted message to break_affine.txt
```

### Example 3: Monoalphabetic Substitution

```bash
# Encrypt with custom alphabet
python ciphers.py mono document.txt e -k ZEBRASCDFGHIJKLMNOPQTUVWXY

# Attack with frequency analysis
python break.py mono cipher_mono.txt
# Analyzes letter frequencies
# Compares with English language statistics
# Outputs most likely decryption
```

---

## 🔬 Technical Details

### Caesar Cipher Implementation

```python
def encrypt_caesar(plaintext, shift):
    result = ""
    for char in plaintext.upper():
        if char.isalpha():
            result += chr((ord(char) - 65 + shift) % 26 + 65)
        else:
            result += char
    return result
```

### Cryptanalysis Methodology

#### 1. Brute Force (Caesar, Affine)
- Try all possible keys
- Validate each attempt against dictionary
- Return first valid plaintext

#### 2. Frequency Analysis (Monoalphabetic)
- Calculate letter frequency in ciphertext
- Compare with English letter distribution
- Map most common ciphertext letters to most common English letters
- Validate mapping with dictionary

#### 3. Dictionary Validation
- Load English word dictionary
- Check if decrypted text contains valid words
- Threshold: ≥60% valid words = successful decryption

---

## 📁 Project Structure

```
Classical-Cryptography-Toolkit/
│
├── src/
│   ├── ciphers.py          # Cipher implementations (encryption/decryption)
│   └── break.py            # Cryptanalysis tools
│
├── BBM465_HW1_2024_Fall.pdf  # Assignment specification
├── report.pdf              # Technical report
├── LICENSE                 # MIT License
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

---

## 🎓 Academic Context

**Course:** BBM 465 - Information Security Laboratory  
**Institution:** Hacettepe University, Computer Engineering Department  
**Semester:** Fall 2024  
**Topics Covered:**
- Classical cryptography
- Cryptanalysis techniques
- Security through obscurity (why it fails)
- Mathematical foundations of cryptography

---

## ⚠️ Security Notice

> **WARNING:** These ciphers are for **educational purposes only** and should **NEVER** be used for real-world encryption.

**Why?**
- ❌ Trivially breakable with modern computing power
- ❌ No protection against frequency analysis
- ❌ Small key space (except monoalphabetic)
- ❌ Deterministic (same plaintext → same ciphertext)
- ❌ No integrity protection
- ❌ Vulnerable to known-plaintext attacks

**For Production Use:**
- ✅ Use **AES** (Advanced Encryption Standard)
- ✅ Use **RSA** for public key encryption
- ✅ Use established cryptographic libraries (PyCryptodome, cryptography)
- ✅ Never roll your own crypto in production!

---

## 🎯 Learning Outcomes

By studying this project, you will understand:

1. **Classical Cryptography Basics**
   - How substitution ciphers work
   - The concept of keys and key space
   - Encryption vs. encoding

2. **Cryptanalysis Techniques**
   - Brute force attacks
   - Statistical analysis (frequency analysis)
   - Dictionary attacks
   - Chosen plaintext attacks

3. **Security Principles**
   - Why security through obscurity fails
   - The importance of large key spaces
   - Perfect secrecy (One-Time Pad)
   - Kerckhoffs's principle

4. **Python Programming**
   - Command-line argument parsing
   - File I/O operations
   - Modular arithmetic
   - Algorithm optimization

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Bugs** - Open an issue describing the problem
2. **Suggest Features** - Share ideas for improvements
3. **Submit Pull Requests** - Fix bugs or add features
4. **Improve Documentation** - Help make explanations clearer

### Contribution Guidelines

- Follow PEP 8 style guide for Python code
- Add comments for complex algorithms
- Include test cases for new features
- Update README if adding new functionality

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**TL;DR:** You can freely use, modify, and distribute this code, even for commercial purposes, as long as you include the original license.

---

## 👤 Author

**Mehmet Oğuz Kocadere**

- 🎓 Computer Engineering Student @ Hacettepe University
- 🔒 Focus: Cybersecurity, Cryptography, Network Security
- 💼 [LinkedIn](https://linkedin.com/in/mehmet-oguz-kocadere)
- 📧 Email: canmehmetoguz@gmail.com
- 🌐 GitHub: [@memo-13-byte](https://github.com/memo-13-byte)

### 🔗 Related Projects

- [File Integrity Checker](https://github.com/memo-13-byte/file-integrity-checker) - RSA digital signatures
- [Secure Flask Auth Portal](https://github.com/memo-13-byte/secure-flask-auth-portal) - 2FA with OTP
- [Hybrid Kerberos System](https://github.com/memo-13-byte/hybrid-kerberos-system) - Enterprise authentication

---

## 🙏 Acknowledgments

- **Hacettepe University** - Computer Engineering Department
- **BBM 465 Course** - Information Security Laboratory
- **Classical Cryptography** - Historical cipher implementations from:
  - Julius Caesar (Caesar Cipher)
  - Al-Kindi (Frequency Analysis, 9th century)
  - Leon Battista Alberti (Polyalphabetic ciphers)

---

## 📊 Statistics

![Python](https://img.shields.io/badge/Python-100%25-blue?style=flat-square)
![Lines of Code](https://img.shields.io/badge/Lines%20of%20Code-500+-green?style=flat-square)
![Commits](https://img.shields.io/github/commit-activity/m/memo-13-byte/Classical-Cryptography-Toolkit?style=flat-square)
![Last Commit](https://img.shields.io/github/last-commit/memo-13-byte/Classical-Cryptography-Toolkit?style=flat-square)

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

**Made with ❤️ for cybersecurity education**

</div>
