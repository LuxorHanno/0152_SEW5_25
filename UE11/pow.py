__author__ = "Hanno Postl"
__version__ = "1.0"
__status__ = "Finished"

import time

def my_pow(a, b, n):
    """
    Berechnet a hoch b modulo n.
    :param a: Basis
    :param b: Exponent
    :param n: Modulo
    :return: Ergebnis der Berechnung
    """
    result = 1
    a = a % n
    while b > 0:
        if b & 1:
            result = (result * a) % n
        b = b >> 1
        a = (a * a) % n
    return result




if __name__ == "__main__":
    # Testwerte
    a = 152679878987343567865343453634
    b = 9875671234567890987654321234567876543212345677656543212345678987654
    n = 19673456434567897654323454

    # Teste die eingebaute pow()-Funktion
    start = time.time()
    print(pow(a, b, n))
    end = time.time()
    print("Built-in pow() time: ", 1000 * (end - start))

    # Teste die benutzerdefinierte my_pow()-Funktion
    start = time.time()
    print(my_pow(a, b, n))
    end = time.time()
    print("Custom my_pow() time: ", 1000000 * (end - start))

    """
    #Testen mir a**b%n
    start = time.time()
    print(a**b % n)
    end = time.time()
    print("Konservativ: ", 1000000 * (end - start))
    """