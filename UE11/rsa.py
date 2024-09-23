__author__ = "Hanno Postl"
__version__ = "1.0"
__status__ = "Finished"

import random
from sqlite3 import enable_callback_tracebacks
from sys import byteorder

from ansible_collections.community.general.plugins.modules.sensu_silence import clear
from ansible_collections.dellemc.openmanage.plugins.modules.ome_application_certificate import read_file

import miller_rabin


def ggt(x: int, y: int) -> int:
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
            print(byte)
            yield int.from_bytes(byte, byteorder="big")


def ints2file(filename, ints, bytelength):
    """
    Writes a list of integers to a file.
    :param filename: The name of the file.
    :param ints: The list of integers.
    """
    with open(filename, "ab") as file:
        for i in ints:
            file.write(i.to_bytes(bytelength, byteorder="big"))

def encryptFile(clearfile, cryptfile, public_key):
    """
    Encrypts a message using the public key.
    :param m: The message to encrypt.
    :param public_key: The public key.
    :return: The encrypted message.
    """
    with open(cryptfile, "w") as file:
        file.write("")
    for i in file2ints(clearfile, public_key[1].bit_length() // 8):
        ints2file(cryptfile, [pow(i, public_key[0], public_key[1])], public_key[1].bit_length() // 8 + 1)

def decryptFile(cryptfile, clearfile, private_key):
    """
    Encrypts a message using the public key.
    :param m: The message to encrypt.
    :param public_key: The public key.
    :return: The encrypted message.
    """
    with open(clearfile, "w") as file:
        file.write("")
    for i in file2ints(cryptfile, private_key[1].bit_length() // 8 +1):
        ints2file(clearfile, [pow(i, private_key[0], private_key[1])], private_key[1].bit_length() // 8)

if __name__ == "__main__":
    private, public, = generate_keys(128)

    encryptFile("Plain.txt", "Encrypted.txt", public)
    decryptFile("Encrypted.txt", "Decrypted.txt", private)
    """
    print(private)
    print(public)
    f = file2ints("Plain.txt", public[1])
    ints2file("Encrypted.txt", f, public[1])
    """
