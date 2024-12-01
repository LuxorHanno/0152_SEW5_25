__author__ = "Hanno Postl"
__version__ = "1.2"
__status__ = "Finished"

import pandas as pd
import unicodedata
import random
import os
import logging
import argparse
from logging.handlers import RotatingFileHandler
from typing import List, Dict

# Argument parser setup
parser = argparse.ArgumentParser(description="Create class users from an Excel file.")
parser.add_argument("input_file", help="Path to the input Excel file")
parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
parser.add_argument("-q", "--quiet", action="store_true", help="Enable quiet logging")
args = parser.parse_args()

# Logging configuration
log_file = "./output/create_class.log"
os.makedirs("./output", exist_ok=True)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG if args.verbose else logging.WARNING if args.quiet else logging.INFO)

handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=5)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(consoleHandler)

def normalize_username(name: str) -> str:
    """
    Normalize a username by replacing German umlauts, converting to lowercase,
    removing accents, and keeping only alphanumeric characters and underscores.

    Parameters:
    name (str): The original username.

    Returns:
    str: The normalized username.
    """
    name = name.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    name = name.lower().replace(" ", "_")
    name = unicodedata.normalize("NFD", name)
    name = ''.join(c for c in name if not unicodedata.combining(c))
    return ''.join(c for c in name if c.isalnum() or c == "_")

def generate_password(class_name: str, room_number: str, advisor: str) -> str:
    """
    Generate a password based on class name, room number, and advisor.

    Parameters:
    class_name (str): The class name.
    room_number (str): The room number.
    advisor (str): The advisor's name.

    Returns:
    str: The generated password.
    """
    specialChars = "!%&(),._-=^#"
    randomChar = random.choice(specialChars)
    return f"{class_name[0]}{randomChar}{room_number[:3]}{advisor[0].upper()}"

def generate_random_password(length: int = 12) -> str:
    """
    Generate a random password of a given length.

    Parameters:
    length (int): The length of the password. Default is 12.

    Returns:
    str: The generated random password.
    """
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!%&(),._-=^#"
    return ''.join(random.choice(chars) for _ in range(length))

# Read class data from the Excel file
try:
    classData: pd.DataFrame = pd.read_excel(args.input_file)
except FileNotFoundError:
    logger.error(f"File not found: {args.input_file}")
    exit(1)

# Prepare script contents
add_script_path: str = "./output/class_add.sh"
del_script_path: str = "./output/class_del.sh"
csv_path: str = "./output/class.csv"

with open(add_script_path, "w") as add_script, open(del_script_path, "w") as del_script:
    add_script.write("#!/bin/bash\n")
    del_script.write("#!/bin/bash\n")

    csv_data: List[Dict[str, str]] = []
    for _, row in (x for x in classData.iterrows() if not pd.isnull(x[1]["Klasse"])):
        class_name: str = str(row["Klasse"])
        room_number: str = str(row["Raum Nr."])
        advisor: str = str(row["KV"])

        username: str = f"k{normalize_username(class_name)}"
        password: str = generate_password(class_name, room_number, advisor)

        homeDir: str = f"/home/klassen/{username}"
        groups: str = "cdrom,plugdev,sambashare"

        add_script.write(
            f"useradd -m -d {homeDir} -s /bin/bash -c '{class_name}' -G {groups} {username}\n"
            f"echo '{username}:{password}' | chpasswd\n"
        )
        del_script.write(f"userdel -r {username}\n")

        csv_data.append({"Username": username, "Password": password, "Home": homeDir})

        logger.debug(f"Created user {username} with password {password} and home directory {homeDir} for class {class_name} in room {room_number} with advisor {advisor}.")

    # Add additional users
    for user in ["lehrer", "seminar"]:
        username: str = user
        password: str = generate_random_password()
        homeDir: str = f"/home/lehrer/{username}"

        add_script.write(
            f"useradd -m -d {homeDir} -s /bin/bash -c '{username}' -G {groups} {username}\n"
            f"echo '{username}:{password}' | chpasswd\n"
        )
        del_script.write(f"userdel -r {username}\n")

        csv_data.append({"Username": username, "Password": password, "Home": homeDir})

# Save CSV
csv_df: pd.DataFrame = pd.DataFrame(csv_data)
csv_df.to_csv(csv_path, index=False)

logger.info("Scripts class_add.sh, class_del.sh, and class.csv successfully created.")