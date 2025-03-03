__author__ = "Hanno Postl"
__version__ = "1.1"
__status__ = "WIP"

import csv
import math
from collections import defaultdict, Counter
from typing import List, Optional, TypeVar, NamedTuple, Dict, Any

import matplotlib.pyplot as plt
import numpy as np


# Define the Candidate class
class Candidate(NamedTuple):
    anfangsbuchstabe: str
    puenktlich: bool
    htl: bool
    sprache: str
    erfolgreich: Optional[bool] = None


# Define a generic type variable
T = TypeVar('T')


# Function to read the CSV file and return a list of Candidate instances
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


def partition_by(inputs: List[T], attribute: str) -> Dict[Any, List[T]]:
    """
    Partition the inputs into lists based on the specified attribute (column name).

    Parameters:
    inputs (List[T]): The list of inputs to partition.
    attribute (str): The attribute to partition by.

    Returns:
    Dict[Any, List[T]]: A dictionary where the keys are unique values of the attribute
                        and the values are lists of inputs with that attribute value.
    """
    partitions: Dict[Any, List[T]] = defaultdict(list)
    for input in inputs:
        key = getattr(input, attribute)  # Get the value of the specified attribute
        partitions[key].append(input)  # Add the input to the corresponding list
    return partitions


def entropy(class_probabilities: List[float]) -> float:
    """
    Calculate the entropy of a list of class probabilities.

    Parameters:
    class_probabilities (List[float]): A list of probabilities for each class.

    Returns:
    float: The entropy value.

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


def draw_entropy():
    """
    Draw the graph of the entropy function H(p) = -p * log2(p) over the interval [0, 1].
    """
    p_values = np.linspace(0, 1, 500)
    entropy_values = [-p * np.log2(p) if p > 0 else 0 for p in p_values]

    plt.figure(figsize=(8, 6))
    plt.plot(p_values, entropy_values, label=r'$H(p) = -p \cdot \log_2(p)$')
    plt.title('Entropy Function')
    plt.xlabel('p')
    plt.ylabel('H(p)')
    plt.grid(True)
    plt.legend()
    plt.show()


def class_probabilities(labels: List[Any]) -> List[float]:
    """
    Calculate the relative frequency of each class in the given list of labels.

    Parameters:
    labels (List[Any]): A list of labels.

    Returns:
    List[float]: A list of relative frequencies of each class.

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


def data_entropy(labels: List[Any]) -> float:
    """
    Calculate the entropy of the given labels.

    Parameters:
    labels (List[Any]): A list of labels.

    Returns:
    float: The entropy value.

    >>> data_entropy(["Huhn"])
    0.0
    >>> data_entropy([1, 1])
    0.0
    >>> data_entropy(["a", "b", "a", "c", "a"])
    1.3709505944546687
    """
    probabilities = class_probabilities(labels)
    return entropy(probabilities)

def partition_entropy(subsets: List[List[Any]]) -> float:
    """
    Calculate the entropy of a partition of subsets.

    Parameters:
    subsets (List[List[Any]]): A list of subsets.

    Returns:
    float: The entropy value of the partition.

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

def partition_entropy_by(inputs: List[Any], attribute: str, label_attribute: str) -> float:
    """
    Calculate the entropy of a partition of inputs by the specified attribute.

    Parameters:
    inputs (List[Any]): The list of inputs to partition.
    attribute (str): The attribute to partition by.
    label_attribute (str): The attribute to use for calculating entropy.

    Returns:
    float: The entropy value of the partition.

    >>> inputs = readfile("res/candidates.csv")
    >>> partition_entropy_by(inputs, 'htl', 'erfolgreich')
    0.8885860757148735
    """
    partitions = partition_by(inputs, attribute)
    labels = [[getattr(input, label_attribute) for input in partition] for partition in partitions.values()]
    return partition_entropy(labels)

# Example usage
if __name__ == "__main__":
    # Read the candidates from the CSV file
    candidates = readfile('res/candidates.csv')

    # Partition the candidates by the 'sprache' attribute
    partitioned_by_sprache = partition_by(candidates, 'sprache')

    # Print the partitioned dictionary
    for key, value in partitioned_by_sprache.items():
        print(f"{key}: {value}")

    # Print Graph of Entropy  # draw_entropy()
