__author__ = "Hanno Postl"
__version__ = "1.6"
__status__ = "Finished"

import argparse
import csv
import math
import sys
from collections import defaultdict, Counter
from typing import List, Optional, TypeVar, Dict, NamedTuple, Union, Any

import matplotlib.pyplot as plt
import numpy as np


# Definiere die Klasse Candidate
class Candidate(NamedTuple):
    anfangsbuchstabe: str
    puenktlich: bool
    htl: bool
    sprache: str
    erfolgreich: Optional[bool] = None


# Definiere einen generischen Typ
T = TypeVar('T')


# Funktion zum Einlesen der CSV-Datei und Rückgabe einer Liste von Candidate-Instanzen
def readfile(filename: str) -> List[T]:
    candidates: List[Candidate] = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            anfangsbuchstabe = row['name'][0]
            puenktlich = row['puenktlich'] == 'ja'
            htl = row['htl'] == 'ja'
            sprache = row['sprache']
            erfolgreich = row['erfolgreich'] == 'ja' if row['erfolgreich'] else None
            candidate = Candidate(anfangsbuchstabe, puenktlich, htl, sprache, erfolgreich)
            candidates.append(candidate)
    return candidates


# Funktion zur Partitionierung der Eingaben basierend auf einem Attribut
def partition_by(inputs: List[T], attribute: str) -> Dict[Any, List[T]]:
    """
    Partitioniere die Eingaben in Listen basierend auf dem angegebenen Attribut (Spaltenname).

    Parameters:
    inputs (List[T]): Die Liste der Eingaben, die partitioniert werden sollen.
    attribute (str): Das Attribut, nach dem partitioniert werden soll.

    Returns:
    Dict[Any, List[T]]: Ein Dictionary, dessen Schlüssel die eindeutigen Werte des Attributs sind
                        und dessen Werte Listen von Eingaben mit diesem Attributswert enthalten.
    """
    partitions: Dict[Any, List[T]] = defaultdict(list)
    for input in inputs:
        key = getattr(input, attribute)  # Hole den Wert des angegebenen Attributs
        partitions[key].append(input)  # Füge die Eingabe der entsprechenden Liste hinzu
    return partitions


# Funktion zur Berechnung der Entropie einer Liste von Klassenwahrscheinlichkeiten
def entropy(class_probabilities: List[float]) -> float:
    """
    Berechnet die Entropie einer Liste von Klassenwahrscheinlichkeiten.

    Parameters:
    class_probabilities (List[float]): Eine Liste von Wahrscheinlichkeiten für jede Klasse.

    Returns:
    float: Der Entropiewert.

    >>> entropy([0.0])
    0.0
    >>> entropy([1.0])
    0.0
    >>> entropy([0.5, 0.5])
    1.0
    >>> entropy([0.2, 0.8])
    0.7219280948873623
    >>> entropy([0.2, 0.7])
    0.8245868399583032
    """
    return float(-sum(p * math.log2(p) for p in class_probabilities if p > 0)) + 0.0


# Funktion zum Zeichnen der Entropiefunktion
def draw_entropy():
    """
    Zeichne den Graphen der Entropiefunktion H(p) = -p * log2(p) im Intervall [0, 1].
    """
    p_values = np.linspace(0, 1, 500)
    entropy_values = [-p * np.log2(p) if p > 0 else 0 for p in p_values]

    plt.figure(figsize=(8, 6))
    plt.plot(p_values, entropy_values, label=r'$H(p) = -p \cdot \log_2(p)$')
    plt.title('Entropiefunktion')
    plt.xlabel('p')
    plt.ylabel('H(p)')
    plt.grid(True)
    plt.legend()
    plt.show()


# Funktion zur Berechnung der relativen Häufigkeit jeder Klasse
def class_probabilities(labels: List[Any]) -> List[float]:
    """
    Berechnet die relative Häufigkeit jeder Klasse in der gegebenen Liste von Labels.

    Parameters:
    labels (List[Any]): Eine Liste von Labels.

    Returns:
    List[float]: Eine Liste von relativen Häufigkeiten jeder Klasse.

    >>> class_probabilities([1])
    [1.0]
    >>> class_probabilities([1, 1])
    [1.0]
    >>> class_probabilities(["a", "b", "a", "c", "a"])
    [0.6, 0.2, 0.2]
    """
    total_count = len(labels)
    count = Counter(labels)
    return [count[label] / total_count for label in count]


# Funktion zur Berechnung der Entropie der gegebenen Labels
def data_entropy(labels: List[Any]) -> float:
    """
    Berechnet die Entropie der gegebenen Labels.

    Parameters:
    labels (List[Any]): Eine Liste von Labels.

    Returns:
    float: Der Entropiewert.

    >>> data_entropy(["Huhn"])
    0.0
    >>> data_entropy([1, 1])
    0.0
    >>> data_entropy(["a", "b", "a", "c", "a"])
    1.3709505944546687
    """
    probabilities = class_probabilities(labels)
    return entropy(probabilities)


# Funktion zur Berechnung der Entropie einer Partition von Subsets
def partition_entropy(subsets: List[List[Any]]) -> float:
    """
    Berechnet die Entropie einer Partition von Subsets.

    Parameters:
    subsets (List[List[Any]]): Eine Liste von Subsets.

    Returns:
    float: Der Entropiewert der Partition.

    >>> partition_entropy([["Huhn"]])
    0.0
    >>> partition_entropy([["Huhn"],["Kuh"]])
    0.0
    >>> partition_entropy([["Huhn"],["Kuh","Katze","Egel","Gelse","Spinne","Biene","Wanze"]])
    2.456435556800403
    >>> partition_entropy([["ja"],["ja","nein","etwas"],["nein","nein", "nein"]])
    0.6792696431662097
    >>> partition_entropy([["ja"],["etwas","etwas","etwas"],["nein","nein", "nein"]])
    0.0
    """
    total_count = sum(len(subset) for subset in subsets)
    return sum((len(subset) / total_count) * data_entropy(subset) for subset in subsets)


# Funktion zur Berechnung der Entropie einer Partition der Eingaben nach einem Attribut
def partition_entropy_by(inputs: List[Any], attribute: str, label_attribute: str) -> float:
    """
    Berechnet die Entropie einer Partition der Eingaben nach dem angegebenen Attribut.

    Parameters:
    inputs (List[Any]): Die Liste der Eingaben, die partitioniert werden sollen.
    attribute (str): Das Attribut, nach dem partitioniert werden soll.
    label_attribute (str): Das Attribut, das für die Berechnung der Entropie verwendet wird.

    Returns:
    float: Der Entropiewert der Partition.

    >>> inputs = readfile("res/candidates.csv")
    >>> partition_entropy_by(inputs, 'htl', 'erfolgreich')
    0.8885860757148734
    """
    partitions = partition_by(inputs, attribute)
    labels = [[getattr(input, label_attribute) for input in partition] for partition in partitions.values()]
    return partition_entropy(labels)


# Funktion zur Bestimmung des Attributs mit minimaler Entropie
def get_partition_min_entropy(inputs: List[Any], attributes: List[str], label_attribute: str) -> tuple[str, float]:
    """
    >>> inputs = readfile("res/candidates.csv")
    >>> get_partition_min_entropy(inputs, ['anfangsbuchstabe', 'puenktlich', 'htl', 'sprache'],'erfolgreich')
    ('puenktlich', 0.5290646583521217)
    """
    min_entropy = float('inf')
    best_attribute = None

    for attribute in attributes:
        entropy_value = partition_entropy_by(inputs, attribute, label_attribute)
        if entropy_value < min_entropy:
            min_entropy = entropy_value
            best_attribute = attribute

    return best_attribute, min_entropy


# Klasse für Blätter im Entscheidungsbaum
class Leaf(NamedTuple):
    value: Any


# Klasse für Knoten im Entscheidungsbaum
class Split(NamedTuple):
    attribute: str
    subtrees: dict
    default_value: Any = None


DecisionTree = Union[Leaf, Split]


# Funktion zur Klassifizierung eines Inputs anhand des Entscheidungsbaums
def classify(tree: DecisionTree, input: Any) -> Any:
    """Klassifiziert den Input anhand des gegebenen Entscheidungsbaums"""
    # Wenn es ein Blatt ist, gib seinen Wert zurück
    if isinstance(tree, Leaf):
        return tree.value
    # Sonst besteht dieser Baum aus einem Attribut, auf das aufgeteilt werden soll
    # und ein Dictionary, dessen Schlüssel Werte dieses Attributs sind
    # und dessen Werte sind die nächsten zu betrachtenden Teilbäume

    subtree_key = getattr(input, tree.attribute)
    if subtree_key not in tree.subtrees:  # Falls es keinen Unterbaum für den Key gibt
        return tree.default_value  # gib den Standardwert zurück

    subtree = tree.subtrees[subtree_key]  # Wähle den passenden Unterbaum aus
    return classify(subtree, input)  # und klassifiziere den Input damit


# Funktion zur Erstellung eines Entscheidungsbaums mit dem ID3-Algorithmus
def build_tree_id3(inputs: List[Any], split_attributes: List[str], target_attribute: str) -> DecisionTree:
    """Generiert mit dem ID3-Algorithmus einen Entscheidungsbaum aus den Inputs"""
    # Zähle die Häufigkeit der Zielattribute
    label_counts = Counter(getattr(input, target_attribute) for input in inputs)
    most_common_label = label_counts.most_common(1)[0][0]
    # Falls es nur ein einziges Label gibt, gib dieses zurück
    if len(label_counts) == 1:
        return Leaf(most_common_label)
    # Falls keine Attribute mehr zum Aufteilen übrig sind, gib das häufigste Label zurück
    if not split_attributes:
        return Leaf(most_common_label)

    # Sonst teile nach dem besten Attribut auf:
    def split_entropy(attribute: str) -> float:
        """Hilfsfunktion zum Finden des besten Attributs"""
        return partition_entropy_by(inputs, attribute, target_attribute)

    best_attribute = min(split_attributes, key=split_entropy)
    partitions = partition_by(inputs, best_attribute)
    new_attributes = [a for a in split_attributes if a != best_attribute]
    # Unterbäume rekursiv aufbauen
    subtrees = {attribute_value: build_tree_id3(subset,
                                                new_attributes,
                                                target_attribute)
                for attribute_value, subset in partitions.items()}
    return Split(best_attribute, subtrees, default_value=most_common_label)


# Hauptfunktion zur Vorhersage mit einem Entscheidungsbaum
def predict_tree():
    parser = argparse.ArgumentParser(description='Predict values using a decision tree.')
    parser.add_argument('training_file', help='CSV file with training data')
    parser.add_argument('predict_file', help='CSV file with data to predict')
    parser.add_argument('output_file', help='CSV file to save predictions')
    args = parser.parse_args()

    # Lese Trainingsdaten ein
    training_data = readfile(args.training_file)

    # Hole Attributnamen aus dem ersten Datensatz
    if not training_data:
        print("Fehler: Trainingsdatei enthält keine Daten")
        sys.exit(1)

    attributes = list(training_data[0]._fields)
    target_attribute = attributes[-1]
    split_attributes = attributes[:-1]

    # Erstelle Entscheidungsbaum
    tree = build_tree_id3(training_data, split_attributes, target_attribute)

    # Lese Vorhersagedaten ein
    predict_data = readfile(args.predict_file)

    # Führe Vorhersagen durch
    results = []
    for data_point in predict_data:
        # Erstelle neuen Datensatz mit der Vorhersage
        prediction = classify(tree, data_point)

        # Hole alle Felder als Dictionary
        data_dict = data_point._asdict()

        # Aktualisiere das Zielattribut mit der Vorhersage
        data_dict[target_attribute] = prediction

        results.append(data_dict)

    # Schreibe Ergebnisse in Ausgabedatei
    with open(args.output_file, 'w', newline='') as file:
        # Verwende denselben Delimiter wie in den Originaldateien
        writer = csv.writer(file, delimiter=';')

        # Schreibe Header-Zeile
        writer.writerow(attributes)

        # Schreibe Datenzeilen
        for data_dict in results:
            writer.writerow([data_dict[attr] for attr in attributes])

    print(f"Vorhersagen gespeichert in {args.output_file}")


# Beispielanwendung
if __name__ == "__main__":
    predict_tree()

    """
    draw_entropy()
    # CSV-Datei einlesen
    candidates = readfile('res/candidates.csv')

    # Kandidaten nach dem Attribut 'sprache' partitionieren
    partitioned_by_sprache = partition_by(candidates, 'sprache')

    for key, value in partitioned_by_sprache.items():
        print(f"{key}: {value}")

    draw_entropy()

# Beispiel-Entscheidungsbaum
    recruiting_tree = Split('sprache', {
        'Java': Split('htl', {
            True: Leaf(True),
            False: Leaf(False)
        }),
        'Whitespace': Leaf(False),
        'Python': Split('puenktlich', {
            False: Leaf(False),
            True: Leaf(True)
        })
    })
    
    input_candidate = Candidate(anfangsbuchstabe='a', sprache='Whitespace', htl=True, puenktlich=True)

    # Klassifizierung des Eingabewerts
    result = classify(recruiting_tree, input_candidate)
    print(result)  # Ausgabe: True
    """