import sys
import argparse

def encrypt_caesar(plaintext, shift):
    """
    Encrypts the given plaintext using the Caesar cipher technique.

    Args:
        plaintext (str): The text to be encrypted.
        shift (int): The number of positions to shift each character.

    Returns:
        str: The encrypted text.
    """
    result = ""
    for char in plaintext:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            result += chr((ord(char) - shift_base - shift) % 26 + shift_base)
        else:
            result += char
    return result


def encrypt_affine(plaintext, a, b):
    """
    Encrypts the given plaintext using the Affine cipher technique.

    Args:
        plaintext (str): The text to be encrypted.
        a (int): The multiplicative key.
        b (int): The additive key.

    Returns:
        str: The encrypted text.
    """
    result = ""
    for char in plaintext:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            result += chr(((a * (ord(char) - shift_base) + b) % 26) + shift_base)
        else:
            result += char
    return result

def encrypt_mono(plaintext, key):
    """
    Encrypts the given plaintext using the Monoalphabetic cipher technique.

    Args:
        plaintext (str): The text to be encrypted.
        key (str): The key alphabet for the Monoalphabetic cipher.

    Returns:
        str: The encrypted text.
    """
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key_map = {alphabet[i]: key[i] for i in range(26)}
    result = ""
    for char in plaintext:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            result += key_map[char.upper()] if char.isupper() else key_map[char.upper()].lower()
        else:
            result += char
    return result



def write_output_file(mode, text):
    """
    Writes the decrypted text to an output file.

    Args:
        mode (str): The mode of decryption (e.g., "caesar", "affine", "mono").
        text (str): The decrypted text to write.
    """
    with open(f'encrypt_{mode}.txt', 'w') as file:
        file.write(text)



def main():
    """
    Main function to parse command-line arguments and perform encryption or decryption
    using Caesar, Affine, or Monoalphabetic ciphers.
    """
    parser = argparse.ArgumentParser(description="Encrypt or decrypt using Caesar, Affine, or Monoalphabetic ciphers.")
    parser.add_argument("cipher", choices=["caesar", "affine", "mono"], help="Cipher technique to use")
    parser.add_argument("file", help="Input file name/path")
    parser.add_argument("mode", choices=["e", "d"], help="Mode: e for encryption, d for decryption")
    parser.add_argument("-s", "--shift", type=int, help="Shift amount for Caesar Cipher")
    parser.add_argument("-a", type=int, help="a value for Affine Cipher")
    parser.add_argument("-b", type=int, help="b value for Affine Cipher")
    parser.add_argument("-k", "--key", help="Key alphabet for Monoalphabetic Cipher")

    args = parser.parse_args()

    with open(args.file, 'r') as f:
        text = f.read()

    if args.cipher == "caesar":
        if args.mode == "e":
            result = encrypt_caesar(text, args.shift % 26)
            write_output_file("caesar", result)

    elif args.cipher == "affine":
        if args.mode == "e":
            result = encrypt_affine(text, args.a, args.b)

    elif args.cipher == "mono":
        if args.mode == "e":
            result = encrypt_mono(text, args.key)


    print(result)


main()