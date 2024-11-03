"""
Author: Hanno Postl
Version: 1.0
Status: finished

This script processes git log data to generate a plot showing the distribution of commits over weekdays and hours.
"""

import argparse
from dateutil import parser
import subprocess
import sys
from collections import defaultdict
from matplotlib import pyplot as plt

def getGitLog(author, path, verbose):
    """
    Retrieves git log data.

    Parameters:
    author (str): The author to filter the commits.
    path (str): The directory of the git repository.
    verbose (bool): If True, prints the git command being run.

    Returns:
    str: The git log output.
    """
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
            print(f"!!Error!! running git log: {stderr.decode('utf-8')}")
            sys.exit(process.returncode)

        return stdout.decode('utf-8')
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def parseGitLog(output):
    """
    Parses the git log output.

    Parameters:
    output (str): The git log output.

    Returns:
    list: A list of dictionaries with 'author' and 'date' keys.
    """
    commits = output.split('-le-')
    parsedCommits = []

    for commit in commits:
        if commit.strip():
            author, date = commit.split(';')
            parsedCommits.append({'author': author.strip(), 'date': date.strip()})

    return parsedCommits

def countCommits(parsed_commits):
    """
    Counts the number of commits per weekday and hour.

    Parameters:
    parsed_commits (list): A list of parsed commits.

    Returns:
    dict: A dictionary with (weekday, hour) as keys and commit counts as values.
    """
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
    """
    Generates and saves a plot of commit counts.

    Parameters:
    commit_counts (dict): A dictionary with (weekday, hour) as keys and commit counts as values.
    author (str): The author of the commits.
    filename (str): The filename to save the plot.
    """
    weekdays = []
    hours = []
    sizes = []

    for (weekday, hour), count in commit_counts.items():
        weekdays.append(weekday)
        hours.append(hour)
        sizes.append(count * 50)

    plt.figure(figsize=(10, 6), dpi=100)
    plt.scatter(hours, weekdays, s=sizes, alpha=0.5)
    plt.xlabel('Uhrzeit')
    plt.ylabel('Wochentag')
    plt.title(f'{author}: {sum(commit_counts.values())} commits')
    plt.xlim(-0.5, 24)
    plt.ylim(-0.5, 6.5)
    plt.yticks(ticks=[0, 1, 2, 3, 4, 5, 6], labels=['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'])
    plt.xticks(range(0, 24, 2))

    plt.grid(True)

    plt.savefig(filename, dpi=72)
    plt.show()

def main():
    """
    Main function to parse arguments, retrieve git log data, and generate the plot.
    """
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

    output = getGitLog(args.author, args.directory, args.verbose)

    if not output:
        print("Keine Commits gefunden.", file=sys.stderr)
        sys.exit(1)

    parsed_commits = parseGitLog(output)

    for commit in parsed_commits:
        print(f"{commit['author']}; {commit['date']}")

    print(f"Anzahl der Commits: {len(parsed_commits)}")

    makePlot(countCommits(parsed_commits), args.author, args.filename)

if __name__ == "__main__":
    main()