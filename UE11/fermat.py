"""
Author: Hanno Postl
Version: 1.0
Status: Under construction
"""
from collections import Counter


def fermat(p):
    """
    Fermat's little theorem states that for any prime number p and any integer a, the number a^p - a is an integer multiple of p.
    This function calculates a^(p-1) mod p for all a in the range from 1 to p.
    :param p: The prime number p.
    :return: A list of the results.
    """
    return [pow(a, p-1, p) for a in range(1, p)]

def stats(values, p):
    """
    Gibt die Werte von a^(p-1) mod p für a = 1...p-1 aus Für jede Primzahl p wird der Prozentsatz der 1en in der
    Liste ausgegeben welche die Wahrscheinlichkeit angibt, dass p eine Primzahl ist.
    :param values: Liste von Werten
    :param p: Primzahl
    """
    count = Counter(values)
    tot = len(values)
    perc = (count[1] / tot) * 100 if 1 in count else 0
    print(f"{p} -> {perc:.2f} % -> res[1]={count[1]},"
          f" len(res)={tot} - {list(count.items())}")


if __name__ == "__main__":
    prim = list(range(2, 12)) + [997]
    carmichael = [9, 15, 21, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562,
                  563, 564, 565, 566, 567, 568, 569, 6601, 8911]

    print("Ergebnisse für Primzahlen von 2 bis 11 und 997:")
    for p in prim:
        stats(fermat(p), p)

    print("\nErgebnisse für Carmichal-Zahlen:")
    for p in carmichael:
        stats(fermat(p), p)