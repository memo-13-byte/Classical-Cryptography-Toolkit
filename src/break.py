import argparse
import math
import random
import re



try_number = 10000
limitnumber = 3

ETAOIN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

english_alphabet = "abcdefghijklmnopqrstuvwxyz"
frequency_ordered_alphabet = "etaoinshrdlcumwfgypbvkjxqz"


def encrypt_caesar(plaintext, shift):
    """
    Encrypts a plaintext using the Caesar cipher with a specified shift.

    Args:
        plaintext (str): The text to be encrypted.
        shift (int): The number of positions to shift each letter.

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


def map_alphabet(alphabet):
    """
    Creates a mapping of characters to their respective indices in an alphabet.

    Args:
        alphabet (str): The alphabet to be mapped.

    Returns:
        dict: A dictionary mapping each character to its index.
    """
    alphabet_map = {}
    for index, character in enumerate(alphabet):
        alphabet_map[character] = index
    return alphabet_map


def map_key_to_alphabet(key, alphabet):
    """
    Maps a key to an alphabet to create a substitution cipher.

    Args:
        key (str): The key to be mapped.
        alphabet (str): The alphabet for the mapping.

    Returns:
        dict: A dictionary mapping each character in the alphabet to the key.

    Raises:
        ValueError: If the key length does not match the alphabet length.
    """
    if len(key) != len(alphabet):
        raise ValueError("Key length must match the alphabet length")
    key_map = {alphabet[i]: key[i] for i in range(len(alphabet))}
    return key_map


def extract_words(dictionary1, alphabet_map):
    """
    Extracts four-letter sequences from the dictionary, counts their occurrences, and creates an index.

    Args:
        dictionary1 (iterable): The dictionary source.
        alphabet_map (dict): A map of the alphabet.

    Returns:
        list: A list of word frequencies indexed by computed values.
    """
    size = 32
    total_elements = size * size * size * size
    spells = [0] * total_elements
    for line in dictionary1:
        line = line.strip().lower()
        if len(line) < 4:
            continue
        for i in range(len(line) - 3):
            spell = line[i:i + 4]
            if all(char in alphabet_map for char in spell):
                index1 = (alphabet_map[spell[0]] << 15) + (alphabet_map[spell[1]] << 10) + (
                            alphabet_map[spell[2]] << 5) + alphabet_map[spell[3]]
                spells[index1] += 1
    return spells


def calculate_and_normalize_words(words_avg):
    """
    Calculates and normalizes word frequencies.

    Args:
        words_avg (list): List of word frequency counts.

    Returns:
        list: Normalized word scores.
    """
    sum_of_words = sum(words_avg)
    minvalue_words = min(val for val in words_avg if val > 0)
    a5 = math.log(minvalue_words / 10 / sum_of_words)
    initial = 0
    for i1, i2 in enumerate(words_avg):
        if i2:
            test = i2 / sum_of_words
            updated = math.log(test) - a5
            words_avg[i1] = updated
            initial += test * updated
    for i1, i2 in enumerate(words_avg):
        words_avg[i1] = round(words_avg[i1] / initial * 1000)
    return words_avg


def char_to_number(txt, alphabet):
    """
    Converts characters in a string to their corresponding numerical values based on an alphabet.

    Args:
        txt (str): The text to convert.
        alphabet (str): The alphabet used for mapping.

    Returns:
        list: List of numerical values corresponding to characters in the text.
    """
    transformmap = {}
    for char, index in enumerate(alphabet.lower()):
        transformmap[index] = char
    result = []
    for index in txt.lower():
        if index in transformmap:
            result.append(transformmap[index])
    return result


def decrypt_bin(key, cipher_bin):
    """
    Decrypts a binary cipher using a given key.

    Args:
        key (list): The decryption key.
        cipher_bin (list): The binary representation of the cipher text.

    Returns:
        list: The decrypted binary data.
    """
    result = []
    for i in cipher_bin:
        result.append(key.index(i))
    return result



def swap_chars(key, index1, index2):
    """
    Swaps two characters in the key at the specified indices.

    Args:
        key (list): The key list where characters will be swapped.
        index1 (int): The index of the first character to swap.
        index2 (int): The index of the second character to swap.
    """
    key[index1], key[index2] = key[index2], key[index1]

def update_plaintext_indices(plaintext, char_positions, char1, index2):
    """
    Updates the indices of a character in the plaintext.

    Args:
        plaintext (list): The plaintext list to update.
        char_positions (list): The positions of characters in the plaintext.
        char1 (int): The character to update.
        index2 (int): The new index for the character.
    """
    for i in char_positions[char1]:
        plaintext[i] = index2

def compute_index(fourthword, char):
    """
    Computes an index based on the fourth word and a character.

    Args:
        fourthword (int): The fourth word value.
        char (int): The character value.

    Returns:
        int: The computed index.
    """
    limitedwords = fourthword % (2 ** 15)
    shiftedword = limitedwords * 32
    result = shiftedword + char
    return result

def fitness_score(plaintext, words):
    """
    Calculates the fitness score of the plaintext based on word frequencies.

    Args:
        plaintext (list): The plaintext list.
        words (list): The list of word frequencies.

    Returns:
        int: The fitness score.
    """
    score = 0
    word_index = (plaintext[0] << 10) + (plaintext[1] << 5) + plaintext[2]
    for char in plaintext[3:]:
        word_index = compute_index(word_index, char)
        score += words[word_index]
    return score

def restore_plaintext(plaintext, char_positions, char, index):
    """
    Restores the plaintext indices for a character.

    Args:
        plaintext (list): The plaintext list to update.
        char_positions (list): The positions of characters in the plaintext.
        char (int): The character to restore.
        index (int): The index to restore the character to.
    """
    update_plaintext_indices(plaintext, char_positions, char, index)


def attempt_key_swap(key, i1, i2, plaintext, char_positions, spells):
    """
    Attempts to swap two characters in the key and evaluates the fitness score.

    Args:
        key (list): The key list where characters will be swapped.
        i1 (int): The index of the first character to swap.
        i2 (int): The index of the second character to swap.
        plaintext (list): The plaintext list to update.
        char_positions (list): The positions of characters in the plaintext.
        spells (list): The list of word frequencies.

    Returns:
        tuple: The temporary matches, first character, and second character.
    """
    char1, char2 = key[i1], key[i2]
    update_plaintext_indices(plaintext, char_positions, char1, i2)
    update_plaintext_indices(plaintext, char_positions, char2, i1)
    tempmatches = fitness_score(plaintext, spells)
    return tempmatches, char1, char2

def evaluate_key(temp_matches, max_matches):
    """
    Evaluates if the temporary matches are greater than the maximum matches.

    Args:
        temp_matches (int): The temporary matches score.
        max_matches (int): The maximum matches score.

    Returns:
        bool: True if temp_matches is greater than max_matches, False otherwise.
    """
    return temp_matches > max_matches

def key_swap_and_evaluation(key, i, i1, plaintext, char_positions, fourwords, max_score):
    """
    Swaps characters in the key and evaluates the new key.

    Args:
        key (list): The key list where characters will be swapped.
        i (int): The index of the first character to swap.
        i1 (int): The index of the second character to swap.
        plaintext (list): The plaintext list to update.
        char_positions (list): The positions of characters in the plaintext.
        fourwords (list): The list of word frequencies.
        max_score (int): The maximum score.

    Returns:
        tuple: The maximum score and a boolean indicating if a better key was found.
    """
    temp_matches, char, char1 = attempt_key_swap(key, i, i1, plaintext, char_positions, fourwords)
    if evaluate_key(temp_matches, max_score):
        swap_chars(key, i, i1)
        return temp_matches, True
    else:
        restore_plaintext(plaintext, char_positions, char, i)
        restore_plaintext(plaintext, char_positions, char1, i1)
        return max_score, False

def frequency_analysis(key, cipher_bin, char_positions, words, alphabet_len, max_try=0):
    """
    Performs frequency analysis to find the best key for decryption.

    Args:
        key (list): The key list to analyze.
        cipher_bin (list): The binary representation of the cipher text.
        char_positions (list): The positions of characters in the plaintext.
        words (list): The list of word frequencies.
        alphabet_len (int): The length of the alphabet.
        max_try (int, optional): The maximum number of tries. Defaults to 0.

    Returns:
        int: The maximum score found.
    """
    plaintext = decrypt_bin(key, cipher_bin)
    found1 = False
    for i in range(alphabet_len - 1):
        for j in range(i + 1, alphabet_len):
            max_try, found_best_key = key_swap_and_evaluation(key, i, j, plaintext, char_positions, words, max_try)
            if found_best_key:
                found1 = True
                break
    if found1:
        return frequency_analysis(key, cipher_bin, char_positions, words, alphabet_len, max_try)
    return max_try

def find_key(ciphertext, alphabet, words):
    """
    Finds the decryption key for the given ciphertext.

    Args:
        ciphertext (str): The ciphertext to decrypt.
        alphabet (str): The alphabet used for the cipher.
        words (list): The list of word frequencies.

    Returns:
        str: The decryption key.
    """
    cipher_bin = char_to_number(ciphertext, alphabet)
    num_chars = len(alphabet)
    char_positions = []
    for i in range(num_chars):
        char_positions.append([])
    for i, j in enumerate(cipher_bin):
        char_positions[j].append(i)
    key_len = len(alphabet)
    curren_max, current_max_shot = 0, 1
    key = list(range(key_len))
    final_key = key.copy()
    for i in range(try_number):
        random.shuffle(key)
        result = frequency_analysis(key, cipher_bin, char_positions, words, key_len)
        if result > curren_max:
            curren_max = result
            current_max_shot = 1
            final_key = key.copy()
        elif result == curren_max:
            current_max_shot += 1
            if current_max_shot == limitnumber:
                break
    result = ""
    for a in final_key:
        result += alphabet[a]
    return result

def key_mapping(decryption_key, alphabet):
    """
    Maps the decryption key to the alphabet.

    Args:
        decryption_key (str): The decryption key.
        alphabet (str): The alphabet used for the cipher.

    Returns:
        dict: A dictionary mapping each character in the alphabet to the decryption key.

    Raises:
        ValueError: If the decryption key length does not match the alphabet length.
    """
    if len(decryption_key) != len(alphabet):
        raise ValueError("The decryption key and the alphabet must have the same length.")
    mapping = {}
    for original_char, mapped_char in zip(alphabet, decryption_key):
        mapping[original_char] = mapped_char
    return mapping

def monoalphabetic_decrypt(ciphered_text, find_key1):
    """
    Decrypts the given ciphered text using the Monoalphabetic cipher technique.

    Args:
        ciphered_text (str): The text to be decrypted.
        find_key1 (dict): The key alphabet for the Monoalphabetic cipher.

    Returns:
        str: The decrypted text.
    """
    decrypted_text = []
    for char in ciphered_text:
        if char.isalpha():
            if char.isupper():
                decrypted_text.append(find_key1[char.lower()].upper())
            else:
                decrypted_text.append(find_key1[char])
        else:
            decrypted_text.append(char)
    return ''.join(decrypted_text)



def extract_potential_words(decoded_text):
    """
    Extracts potential words from the decoded text.

    Args:
        decoded_text (str): The decoded text.

    Returns:
        list: A list of potential words.
    """
    words = re.findall(r'\b[a-zA-Z]+\b', decoded_text)
    return words

def load_dictionary():
    """
    Loads the dictionary from a file.

    Returns:
        set: A set of dictionary words.
    """
    with open('dictionary.txt', 'r') as file:
        dictionary_words = set(word.strip().lower() for word in file)
    return dictionary_words


def extract_longest_word(text):
    """
    Extracts the longest word from the text.

    Args:
        text (str): The text to extract the longest word from.

    Returns:
        str: The longest word, or None if no word is found.
    """
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    return max(words, key=len) if words else None



def decrypt_caesar(ciphertext, dictionary):
    """
    Decrypts the given ciphertext using the Caesar cipher technique.

    Args:
        ciphertext (str): The text to be decrypted.
        dictionary (set): The set of dictionary words.

    Returns:
        str: The decrypted text, or None if no valid decryption is found.
    """
    dictionary = load_dictionary()
    first_word = extract_longest_word(ciphertext)
    if not first_word:
        print("No valid word found in ciphertext.")
        return None

    for shift in range(26):
        decrypted_word = encrypt_caesar(first_word, shift)
        if decrypted_word.lower() in dictionary:
            print(f"Shift {shift}: '{decrypted_word}' is a valid word. Decrypting the entire text...")
            decrypted_text = encrypt_caesar(ciphertext, shift).strip()
            print(decrypted_text)
            return decrypted_text

    print("No valid decryption found.")
    return None








def validate_text(input_text, dictionary):
    """
    Validates the input text by redacting words that are not found in the provided dictionary.

    Args:
        input_text (str): The text to be validated.
        dictionary (set): A set of valid dictionary words.

    Returns:
        str: The validated text with non-dictionary words redacted.
    """
    def replace_match(match):
        word = match.group(0).strip('.,!?')
        if word.lower() not in dictionary and word.isalpha():
            return "[REDACTED]" + match.group(0)[len(word):]
        return match.group(0)

    return re.sub(r"\b\w+['\w-]*[.,!?]?\b", replace_match, input_text)


def mod_inverse(a, m):
    """
    Finds the modular inverse of a with respect to m.

    Args:
        a (int): The number to find the modular inverse of.
        m (int): The modulus.

    Returns:
        int: The modular inverse, or None if no inverse exists.
    """
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def coprime_with_26(a):
    """
    Checks if a is coprime with 26.

    Args:
        a (int): The number to check.

    Returns:
        bool: True if a is coprime with 26, False otherwise.
    """
    return mod_inverse(a, 26) is not None

def decrypt_affine_single_word(ciphertext):
    """
    Decrypts the given ciphertext using the Affine cipher technique by brute-forcing the key.

    Args:
        ciphertext (str): The text to be decrypted.

    Returns:
        str: The decrypted text, or None if no valid decryption is found.
    """
    dictionary = load_dictionary()
    words = extract_first_two_words(ciphertext)

    for a in range(1, 26):
        if coprime_with_26(a):
            for b in range(26):
                a_inv = mod_inverse(a, 26)
                if a_inv is None:
                    continue

                decrypted_words = []
                for word in words:
                    decrypted_word = ""
                    for char in word:
                        if char.isalpha():
                            shift_base = 65 if char.isupper() else 97
                            decrypted_word += chr((a_inv * (ord(char) - shift_base - b) % 26) + shift_base)
                        else:
                            decrypted_word += char

                    decrypted_words.append(decrypted_word)

                if all(decrypted_word.lower() in dictionary for decrypted_word in decrypted_words):
                    return decrypt_affine_with_keys(ciphertext, a, b)

    return None

def extract_first_two_words(ciphertext):
    """
    Extracts the first two words from the ciphertext.

    Args:
        ciphertext (str): The ciphertext to extract words from.

    Returns:
        list: A list of the first two words.
    """
    words = ciphertext.split()
    return words[:2] if len(words) >= 2 else words

def decrypt_affine_with_keys(ciphertext, a, b):
    """
    Decrypts the given ciphertext using the Affine cipher technique with specified keys.

    Args:
        ciphertext (str): The text to be decrypted.
        a (int): The multiplicative key.
        b (int): The additive key.

    Returns:
        str: The decrypted text, or None if no valid decryption is found.
    """
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        return None

    result = ""
    for char in ciphertext:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            result += chr((a_inv * (ord(char) - shift_base - b) % 26) + shift_base)
        else:
            result += char

    return result

def decrypt_affine(ciphertext):
    """
    Decrypts the given ciphertext using the Affine cipher technique by brute-forcing the key.

    Args:
        ciphertext (str): The text to be decrypted.

    Returns:
        str: The decrypted text, or None if no valid decryption is found.
    """
    return decrypt_affine_single_word(ciphertext)



def break_mono(ciphertext, key_alphabet_map):
    """
    Decrypts the given ciphertext using the Monoalphabetic cipher technique.

    Args:
        ciphertext (str): The text to be decrypted.
        key_alphabet_map (dict): The key alphabet map for the Monoalphabetic cipher.

    Returns:
        str: The decrypted text.
    """
    decoded_text = monoalphabetic_decrypt(ciphertext, key_alphabet_map)
    return decoded_text

def write_output_file(mode, text):
    """
    Writes the decrypted text to an output file.

    Args:
        mode (str): The mode of decryption (e.g., "caesar", "affine", "mono").
        text (str): The decrypted text to write.
    """
    with open(f'break_{mode}.txt', 'w') as file:
        file.write(text)

def main():
    """
        The main function that parses command-line arguments to encrypt or decrypt
        text using Caesar, Affine, or Monoalphabetic ciphers. It reads the input file,
        applies the appropriate decryption method based on the selected cipher, and
        writes the output to a file.

        Command-line Arguments:
            cipher (str): The cipher technique to use. Can be "caesar", "affine", or "mono".
            file (str): The name or path of the input file containing the text to be processed.

        Steps:
            1. Parse command-line arguments to determine the cipher type and input file.
            2. Read the content from the specified input file.
            3. Load the dictionary and map the English alphabet.
            4. Based on the chosen cipher, execute the following:
                - For "caesar": Use `decrypt_caesar` to decrypt the text, validate the result, and write to a file.
                - For "affine": Use `decrypt_affine` to decrypt the text, validate the result, and write to a file.
                - For "mono": Read the dictionary file, extract and normalize words, find the decryption key,
                  map the key alphabet, decrypt using `break_mono`, validate the result, and write to a file.
            5. Output files are named based on the cipher used.

        Returns:
            None
        """
    parser = argparse.ArgumentParser(description="Encrypt or decrypt using Caesar, Affine, or Monoalphabetic ciphers.")
    parser.add_argument("cipher", choices=["caesar", "affine", "mono"], help="Cipher technique to use")
    parser.add_argument("file", help="Input file name/path")

    args = parser.parse_args()

    with open(args.file, 'r') as f:
        ciphertext = f.read()

        dictionary = load_dictionary()
        alphabet_map = map_alphabet(english_alphabet)
        spells1 = extract_words(dictionary, alphabet_map)


    if args.cipher == "caesar":
        decrypted_text = decrypt_caesar(ciphertext, dictionary)
        if decrypted_text:
            result2 = validate_text(decrypted_text, dictionary)
            if result2:
                write_output_file("caesar", result2)

    elif args.cipher == "affine":
        decryption = decrypt_affine(ciphertext)
        if decryption:
            result3 = validate_text(decryption, dictionary)
            if result3:
                write_output_file("affine", result3)

    elif args.cipher == "mono":
        dictionary = load_dictionary()
        # dictionary = dictionary_fh.read()
        alphabet_map = map_alphabet(english_alphabet)
        spells1 = extract_words(dictionary, alphabet_map)
        spells1 = calculate_and_normalize_words(spells1)

        final_key1 = find_key(ciphertext, english_alphabet, spells1)
        key_alphabet_map = key_mapping(english_alphabet, final_key1)
        plain_text = break_mono(ciphertext, key_alphabet_map)
        result5 = validate_text(plain_text, dictionary)
        if result5:
            write_output_file("mono", result5)


main()