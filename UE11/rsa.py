__author__ = "Hanno Postl"
__version__ = "1.0"
__status__ = "Finished"

import logging
import pickle
import random
import argparse
from pathlib import Path
import miller_rabin


def ggt(x: int, y: int) -> int:
    """
    Calculate the greatest common divisor of two numbers.
    :param x: Number 1
    :param y: Number 2
    :return: GGT of x and y

    >>> ggt(123456789, 987654321)
    9
    """
    while y != 0:
        x, y = y, x % y
    return x


def generate_keys(number_of_bits):
    """
    Generates a pair of RSA keys.
    :param number_of_bits: The bit length of the keys.
    :return: A tuple containing the private and public key.
    >>> private, public = generate_keys(128)
    >>> d, n, _ = private
    >>> e, n, _ = public
    >>> for x in [239876563, 13123456789009876544657473, 12328753224, 123309876543954345678767654565456543412]:
    ...     c = pow(x, e, n)
    ...     y = pow(c, d, n)
    ...     assert x == y
    """
    n = 0
    while n.bit_length() <= number_of_bits:
        p, q = miller_rabin.generate_prime(number_of_bits // 2 + 1), miller_rabin.generate_prime(number_of_bits // 2)
        n = p * q
    phin = (p - 1) * (q - 1)

    def gen_encryptionkey(bit_length):
        while True:
            prime_candidate = random.getrandbits(bit_length)
            # Set the two most significant bits to 1 to ensure the number has the correct bit length
            prime_candidate |= (1 << (bit_length - 1)) | 1
            if ggt(prime_candidate, phin) == 1:
                return prime_candidate

    e = gen_encryptionkey(number_of_bits)
    d = pow(e, -1, phin)
    return (d, n, d.bit_length()), (e, n, e.bit_length())

def file2ints(filename, bytelength):
    """
    Reads a file and converts it to a list of integers.
    :param filename: The name of the file.
    :return: A list of integers.
    """
    with open(filename, "rb") as file:
        while (byte := file.read(bytelength)):
            yield int.from_bytes(byte, byteorder="big")


def ints2file(filename, ints, bytelength):
    """
    Writes a list of integers to a file.
    :param filename: The name of the file.
    :param ints: The list of integers.
    """
    with open(filename, "ab") as file:
        for i in ints:
            byte_data = i.to_bytes(bytelength, byteorder="big")
            file.write(byte_data)

def encryptFile(clearfile, cryptfile, public_key):
    """
    Encrypts a message using the public key.
    :param m: The message to encrypt.
    :param public_key: The public key.
    :return: The encrypted message.
    """
    with open(cryptfile, "w") as file:
        file.write("")
    remove_null_characters(clearfile)
    for i in file2ints(clearfile, public_key[1].bit_length() // 8):
        ints2file(cryptfile, [pow(i, public_key[0], public_key[1])], public_key[1].bit_length() // 8)

def decryptFile(cryptfile, clearfile, private_key):
    """
    Encrypts a message using the public key.
    :param m: The message to encrypt.
    :param public_key: The public key.
    :return: The encrypted message.

    >>> private, public = generate_keys(1024)
    >>> encryptFile("Plain.txt", "Plain.enc", public)
    >>> decryptFile("Plain.enc", "Plaind.txt", private)
    >>> with open("Plain.txt", "rb") as f1, open("Plaind.txt", "rb") as f2:
    ...     assert f1.read() == f2.read()
    """
    with open(clearfile, "w") as file:
        file.write("")
    for i in file2ints(cryptfile, private_key[1].bit_length() // 8):
        ints2file(clearfile, [pow(i, private_key[0], private_key[1])], private_key[1].bit_length() // 8)
    remove_null_characters(clearfile)


def remove_null_characters(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
    cleaned_content = content.replace('\0', '')

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)


def save_key(key, filename):
    """
    Save the RSA key to a file.
    """
    with open(filename, 'wb') as f:
        pickle.dump(key, f)

def load_key(filename):
    """
    Load the RSA key from a file.
    """
    with open(filename, 'rb') as f:
        return pickle.load(f)


def main():
    parser = argparse.ArgumentParser(description="RSA Encryption/Decryption Tool")

    parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="store_true")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-k", "--keygen", help="generate new RSA keys with the given bit length", type=int)
    group.add_argument("-e", "--encrypt", help="encrypt a file")
    group.add_argument("-d", "--decrypt", help="decrypt a file")

    args = parser.parse_args()

    if args.verbosity:
        logging.basicConfig(level=logging.INFO)
        logging.info("Verbosity turned on")

    # Key generation
    if args.keygen:
        logging.info(f"Generating RSA keys of length {args.keygen} bits...")
        private_key, public_key = generate_keys(args.keygen)

        # Save the keys
        save_key(private_key, 'private_key.pem')
        save_key(public_key, 'public_key.pem')
        logging.info(f"Keys saved to 'private_key.pem' and 'public_key.pem'.")

    # File encryption
    elif args.encrypt:
        logging.info(f"Encrypting file: {args.encrypt}")
        if not Path("public_key.pem").is_file():
            logging.error("Public key not found. Please generate keys first.")
            return

        public_key = load_key('public_key.pem')
        output_file = args.encrypt + ".enc"
        encryptFile(args.encrypt, output_file, public_key)
        logging.info(f"File encrypted to: {output_file}")

    # File decryption
    elif args.decrypt:
        logging.info(f"Decrypting file: {args.decrypt}")
        if not Path("private_key.pem").is_file():
            logging.error("Private key not found. Please generate keys first.")
            return

        private_key = load_key('private_key.pem')
        output_file = args.decrypt.replace(".enc", "")  # Removing the .enc extension
        decryptFile(args.decrypt, output_file, private_key)
        logging.info(f"File decrypted to: {output_file}")


#if __name__ == "__main__":
    #main()