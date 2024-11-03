__author__ = "Hanno Postl"
__version__ = "1.0"
__status__ = ("work in progress")

import argparse
import csv
import xml.etree.ElementTree as ET
from typing import List

def readCSV(file, tal=None, spitze=None) -> list:
    trackPoints = []
    with open(file, 'r') as f:
        if tal and spitze:
            for line in f:
                x = line.split(';')
                if tal <= float(x[3]) and float(x[3]) <= spitze:
                    trackPoints.append(x)
        elif tal:
            for line in f:
                if tal <= line[3]:
                    trackPoints.append(csv.reader(line, delimiter=';'))
        elif spitze:
            for line in f:
                if line[3] <= spitze:
                    trackPoints.append(csv.reader(line, delimiter=';'))
        else:
            trackPoints = csv.reader(f, delimiter=';')
    return trackPoints



def readGPX(file_path: str, tal=None, spitze=None) -> List[List[str]]:
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



def main():
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
        print(data)
    elif fileExt == 'csv':
        data = readCSV(args.infile, args.tal, args.spitze)
        print(data)
    else:
        print('Dateiformat nicht unterstützt')

    #Write data to csv-file
    if args.out.split('.')[-1] == 'csv':
        with open(args.out, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(data)


if __name__ == "__main__":
    main()