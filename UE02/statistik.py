__author__ = "Hanno Postl"
__version__ = "1.0"
__status__ = "finished"

import argparse
from dateutil import parser
import subprocess
import sys
from collections import defaultdict
from matplotlib import pyplot as plt

def getGitLog(author, path, verbose):
    gc = ['git']

    if path:
        gc.extend(['-C', path])

    gc.extend(['log', '--pretty=%an;%ad-le-', '--date=rfc'])

    if author:
        gc.append(f'--author={author}')

    if verbose:
        print(f"Running command: {''.join(gc)}")

    try:
        process = subprocess.Popen(gc, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"Error running git log: {stderr.decode('utf-8')}")
            sys.exit(1)

        return stdout.decode('utf-8')
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def parseGitLog(output):
    commits = output.split('-le-')
    parsedCommits = []

    for commit in commits:
        if commit.strip():
            author, date = commit.split(';')
            parsedCommits.append({'author': author.strip(), 'date': date.strip()})

    return parsedCommits

def countCommits(parsed_commits):
    commit_counts = {}

    for commit in parsed_commits:
        commit_date = parser.parse(commit['date'])
        weekday = commit_date.weekday()
        hour = commit_date.hour
        key = (weekday, hour)

        if key not in commit_counts:
            commit_counts[key] = 0

        commit_counts[key] += 1

    return commit_counts


def makePlot(commit_counts, author, filename):
    weekdays = []
    hours = []
    sizes = []

    for (weekday, hour), count in commit_counts.items():
        weekdays.append(weekday)
        hours.append(hour)
        sizes.append(count * 50)

    plt.xlabel('Uhrzeit')
    plt.ylabel('Wochentag')
    plt.title(f'{author}: {sum(commit_counts.values())} commits')
    plt.xlim(-0.5, 24)
    plt.ylim(-0.5, 6.5)
    plt.yticks(ticks=[0, 1, 2, 3, 4, 5, 6], labels=['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'])
    plt.xticks(range(0, 24, 2))
    plt.figure(figsize=(10, 6), dpi=100)
    plt.scatter(hours, weekdays, s=sizes, alpha=0.5)
    plt.grid(True)

    if filename:
        plt.savefig(filename, dpi=72)
    plt.show()

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
