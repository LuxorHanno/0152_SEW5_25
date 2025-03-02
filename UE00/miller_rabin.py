"""
Author: Hanno Postl
Version: 1.2
Status: Finished
"""
import random

FIRST_100_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                    31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
                    73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
                    127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
                    179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
                    233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
                    283, 293, 307, 311, 313, 317, 331, 337, 347, 349,
                    353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
                    419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
                    467, 479, 487, 491, 499, 503, 509, 521, 523, 541]

def is_prime(n: int) -> bool:
    """
    Check if a number is prime.
    :param n: The number to check.
    :return: True if the number is prime, False otherwise.
    """
    for prime in FIRST_100_PRIMES:
        if n % prime == 0:
            return n == prime
    return is_prim_millerrabin(n) == "probably prime"

def is_prim_millerrabin(number, iterations=20):
    """
    Check if a number is prime using the Miller-Rabin primality test.
    :param number: The number to check.
    :param iterations: The number of iterations to perform.
    :return: "prime" if the number is prime, "composite" if it is composite, "probably prime" if it is probably prime.
    """
    if number < 2 or number % 2 == 0:
        return "not prime"

    #n = d * 2^s + 1
    d, s = number-1, 0
    while d % 2 == 0:
        d //= 2
        s += 1

    def is_composite(a, d, s, n):
        x = pow(a,d,n)
        for _ in range(s):
            y = pow(x,2,n)
            if y == 1 and x != 1 and x != n - 1:
                return True
            x = y
        if x != 1:
            return True
        return False



    for i in range(iterations):
        base = random.randint(2, number-1)
        if is_composite(base,d,s,number):
            return "composite"
    return "probably prime"



def generate_prime(bit_length):
    """
    Generate a prime number with a given bit length.
    :param bit_length: The bit length of the prime number.
    :return: The prime number.
    """
    while True:
        prime_candidate = random.getrandbits(bit_length)
        # Set the two most significant bits to 1 to ensure the number has the correct bit length
        prime_candidate |= (1 << (bit_length - 1)) | 1
        if is_prime(prime_candidate):
            return prime_candidate



if __name__ == '__main__':
    print("Teste Miller-Rabin-Algorithmus:")
    test_numbers = [221, 24566544301293569, 2512, 797]
    for number in test_numbers:
        print(f"Die Zahl {number} ist {'eine Primzahl' if is_prime(number) else 'keine Primzahl'}")

    print("\nErste Primzahl mit mehr als 512 Bits:")
    number = pow(2, 512) + 1
    while not is_prime(number):
        number += 2
    print(number)

    number = 24566544301293569

    # Überprüfen, ob die Zahl eine Primzahl ist
    is_prime_number = is_prime(number)
    print(f"Ist {number} eine Primzahl? {'Ja' if is_prime_number else 'Nein'}")

    # Die Zahl in eine Binärzahl umwandeln und in Segmente von 12 Zeichen aufteilen
    binary = bin(number)[2:]
    print("\nDie Zahl als Binärzahl mit 12 Zeichen/Zeile:")
    for i in range(0, len(binary), 12):
        print(binary[i:i + 12])

    # Die nächsthöhere Primzahl bestimmen
    next_prime = number + 1
    while not is_prime(next_prime):
        next_prime += 1
    print(f"\nDie nächsthöhere Primzahl ist {next_prime}")

    # Überprüfen, ob die nächsthöhere Primzahl die gleiche Nachricht enthält
    binary = bin(next_prime)[2:]
    print("\nDie nächsthöhere Primzahl als Binärzahl mit 12 Zeichen/Zeile:")
    for i in range(0, len(binary), 12):
        print(binary[i:i + 12])

    # Massage: HTL