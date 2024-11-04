__author__ = "Hanno Postl"
__version__ = "1.1"
__status__ = "work in progress"

import argparse
import csv
import xml.etree.ElementTree as ET
from typing import List, Optional
import matplotlib.pyplot as plt

def readCSV(file: str, tal: Optional[float] = None, spitze: Optional[float] = None) -> List[List[str]]:
    """
    Reads a CSV file and filters track points based on elevation.

    Parameters:
    file (str): The path to the CSV file.
    tal (float, optional): The minimum elevation to filter track points.
    spitze (float, optional): The maximum elevation to filter track points.

    Returns:
    List[List[str]]: A list of track points.
    """
    trackPoints = []
    with open(file, 'r') as f:
        if tal and spitze:
            for line in f:
                x = line.split(';')
                if tal <= float(x[3]) and float(x[3]) <= spitze:
                    trackPoints.append(x)
        elif tal:
            for line in f:
                if tal <= float(line.split(';')[3]):
                    trackPoints.append(line.split(';'))
        elif spitze:
            for line in f:
                if float(line.split(';')[3]) <= spitze:
                    trackPoints.append(line.split(';'))
        else:
            trackPoints = list(csv.reader(f, delimiter=';'))
    return trackPoints

def readGPX(file_path: str, tal: Optional[float] = None, spitze: Optional[float] = None) -> List[List[str]]:
    """
    Reads a GPX file and filters track points based on elevation.

    Parameters:
    file_path (str): The path to the GPX file.
    tal (float, optional): The minimum elevation to filter track points.
    spitze (float, optional): The maximum elevation to filter track points.

    Returns:
    List[List[str]]: A list of track points.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    namespace = {'default': 'http://www.topografix.com/GPX/1/1'}

    trackPoints = []

    for trkpt in root.findall('.//default:trkpt', namespace):
        time = trkpt.find('default:time', namespace).text
        lon = trkpt.attrib['lon']
        lat = trkpt.attrib['lat']
        ele = trkpt.find('default:ele', namespace).text

        if tal and spitze:
            if tal <= float(ele) and float(ele) <= spitze:
                trackPoints.append([time, lon, lat, ele])
        elif tal:
            if tal <= float(ele):
                trackPoints.append([time, lon, lat, ele])
        elif spitze:
            if float(ele) <= spitze:
                trackPoints.append([time, lon, lat, ele])
        else:
            trackPoints.append([time, lon, lat, ele])

    return trackPoints

def makePlot(data: List[List[str]], marker: bool, dot: Optional[str], connect: bool, line: Optional[str], filename: Optional[str] = None) -> None:
    """
    Generates and saves a plot of track points.

    Parameters:
    data (List[List[str]]): The track points data.
    marker (bool): Whether to mark the first and last points.
    dot (str, optional): The RGB color of the points.
    connect (bool): Whether to connect the points with lines.
    line (str, optional): The RGB color of the lines.
    filename (str, optional): The filename to save the plot.
    """
    x = [float(point[1]) for point in data]
    y = [float(point[2]) for point in data]

    colors = tuple([int(c) / 255 for c in dot.split(',')]) if dot else (0, 0, 1)
    line_color = tuple([int(c) / 255 for c in line.split(',')]) if line else (0, 1, 0)

    plt.scatter(x, y, color=[colors], alpha=0.5)
    if connect:
        plt.plot(x, y, color=line_color, alpha=0.5)
    if marker:
        plt.scatter([x[0], x[-1]], [y[0], y[-1]], color="red", marker="x")

    if not filename:
        filename = "untitled"
    plt.savefig(filename, dpi=702)

def main() -> None:
    """
    Main function to parse arguments, read input files, and generate plots or CSV files.
    """
    parser = argparse.ArgumentParser(
        description="skitrack by Hanno Postl / HTL Rennweg"
    )
    parser.add_argument(
        'infile',
        type=str,
        help='Input-Datei (z.B. track.gpx oder track.csv)'
    )
    parser.add_argument(
        '-o', '--out',
        type=str,
        help='Zu generierende Datei, z.B. ski.csv oder ski.png'
    )
    parser.add_argument(
        '-m', '--marker',
        action='store_true',
        help='Sollen der erste und letzte Punkt markiert werden?'
    )
    parser.add_argument(
        '-t', '--tal',
        type=float,
        help='Seehöhe des niedrigsten Punktes, der noch ausgewertet werden soll'
    )
    parser.add_argument(
        '-s', '--spitze',
        type=float,
        help='Seehöhe des höchsten Punktes, der noch ausgewertet werden soll'
    )
    parser.add_argument(
        '-d', '--dot',
        type=str,
        help='RGB-Farbe der Punkte z.B.: 128,128,255'
    )
    parser.add_argument(
        '-c', '--connect',
        action='store_true',
        help='Sollen die Bildpunkte mit Linien verbunden werden?'
    )
    parser.add_argument(
        '-l', '--line',
        type=str,
        help='RGB-Farbe der Linien z.B.: 255,128,255'
    )
    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Zeigt Details an (siehe Angabe)'
    )
    verbosity_group.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='keine Textausgabe'
    )

    args = parser.parse_args()
    fileExt = args.infile.split('.')[-1]
    if fileExt == 'gpx':
        data = readGPX(args.infile, args.tal, args.spitze)
    elif fileExt == 'csv':
        data = readCSV(args.infile, args.tal, args.spitze)
    else:
        print('Dateiformat nicht unterstützt')
        return

    print("Niedrigster Punkt: ", min(data, key=lambda x: float(x[3]))[3])
    print("Höchster Punkt: ", max(data, key=lambda x: float(x[3]))[3])
    print("Anzahl der Punkte: ", len(data))

    # Write data to csv-file
    if args.out:
        if args.out.split('.')[-1] == 'csv':
            with open(args.out, 'w') as f:
                writer = csv.writer(f)
                writer.writerows(data)
        elif args.out.split('.')[-1] == 'png':
            makePlot(data, args.marker, args.dot, args.connect, args.line, args.out)

if __name__ == "__main__":
    main()