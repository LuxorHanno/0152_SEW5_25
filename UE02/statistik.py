__author__ = "Hanno Postl"
__version__ = "1.0"
__status__ = "finished"

import argparse
from dateutil import parser
import subprocess
import sys
from collections import defaultdict
from matplotlib import pyplot as plt


def main():
    parser = argparse.ArgumentParser(
        description="statistik.py by Hanno Postl 5CN -- draws a plot with git log data"
    )
    parser.add_argument('-a', '--author',
        type=str,
        default="",
        help='The author to filter the commits, default=""'
    )
    parser.add_argument(
        '-d', '--directory',
        type=str,
        default=".",
        help='The directory of the git repository, default="."'
    )
    parser.add_argument(
        '-f', '--filename',
        type=str,
        help='The filename of the plot. Don’t save picture if parameter is missing'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='increase verbosity'
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='decrease verbosity'
    )

    args = parser.parse_args()

    # Git log Daten abrufen
    output = getGitLog(args.author, args.directory, args.verbose)

    if not output:
        print("Keine Commits gefunden.", file=sys.stderr)
        sys.exit(1)

    # Daten parsen
    parsed_commits = parseGitLog(output)

    # Ergebnisse ausgeben
    for commit in parsed_commits:
        print(f"{commit['author']}; {commit['date']}")

    print(f"Anzahl der Commits: {len(parsed_commits)}")

    makePlot(countCommits(parsed_commits), args.author, args.filename)


if __name__ == "__main__":
    main()
