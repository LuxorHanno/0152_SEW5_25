__author__ = "Hanno Postl"
__version__ = "1.1"
__status__ = "Finished"

from argparse import ArgumentParser
from time import sleep, perf_counter_ns
from xml.etree.ElementPath import prepare_self
from xml.sax import default_parser_list


def fromStrings(strings: list[str]) -> list[list[int]]:
    return [[ord(c) for c in line] for line in [str.strip() for str in strings]]

def labFromFile(path: str) -> list[list[int]]:
    with open(path, "r") as file:
        return fromStrings(file.readlines())

def printLab(lab: list[list[int]]):
    for row in lab:
        print("".join([chr(c) for c in row]))

def suchen(zeile: int, spalte: int, lab: list[list[int]], print: bool = False, delay: int = 1) -> bool:
    if lab[zeile][spalte] == ord('A'):
        return True

    if lab[zeile][spalte] == ord('#') or lab[zeile][spalte] == ord('.'):
        return False

    lab[zeile][spalte] = ord('.')

    if print:
        printLab(lab)
        sleep(delay / 1000)

    hit: bool = (suchen(zeile, spalte + 1, lab) or
          suchen(zeile + 1, spalte, lab) or
          suchen(zeile, spalte - 1, lab) or
          suchen(zeile - 1, spalte, lab))

    lab[zeile][spalte] = ord(' ')

    return hit

def alleSuchen(zeile: int, spalte: int, lab: list[list[int]], print: bool = False, delay: int = 500) -> int:
    if lab[zeile][spalte] == ord('A'):
        return 1

    if lab[zeile][spalte] == ord('#') or lab[zeile][spalte] == ord('.'):
        return 0

    lab[zeile][spalte] = ord('.')

    if print:
        printLab(lab)
        sleep(delay/1000)

    hit: int = (alleSuchen(zeile, spalte + 1, lab, print, delay) +
          alleSuchen(zeile + 1, spalte, lab, print, delay) +
          alleSuchen(zeile, spalte - 1, lab, print, delay) +
          alleSuchen(zeile - 1, spalte, lab, print, delay))

    lab[zeile][spalte] = ord(' ')

    return hit




if __name__ == "__main__":
    parser = ArgumentParser(description="calculate number of ways through a labyrinth")
    parser.add_argument("filename", type=str, help="file containing the labyrinth to solve")
    parser.add_argument("-x", "--xstart", type=int, help="x-coordinae to start")
    parser.add_argument("-y", "--ystart", type=int, help="y-coordinae to start")
    parser.add_argument("-p", "--print", help="print output of every soslution", action='store_true')
    parser.add_argument("-t", "--time", help="print total calculation time (in milliseconds)", action='store_true')
    parser.add_argument("-d", "--delay", type=int, default=500, help="delay after printing a solution (in milliseconds)")

    args = parser.parse_args()
    lab: list[list[int]] = labFromFile(args.filename)
    start_time = perf_counter_ns()
    hits: int = alleSuchen(args.ystart,args.xstart,lab,args.print,args.delay)
    end_time = perf_counter_ns()
    print(f"Anzahl Wege: {hits}"
          f"{f" in {(end_time - start_time)/1000} Millisekunden" if args.time else ''}")
