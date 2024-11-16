__author__ = "Hanno Postl"
__version__ = "1.0"
__status__ = "under construction"

import pandas as pd
import unicodedata
import random
import os
import logging
import argparse
from logging.handlers import RotatingFileHandler

# Argument parser setup
parser = argparse.ArgumentParser(description="Create class users from an Excel file.")
parser.add_argument("input_file", help="Path to the input Excel file")
parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
parser.add_argument("-q", "--quiet", action="store_true", help="Enable quiet logging")
args = parser.parse_args()

