__author__ = "Hanno Postl"
__version__ = "1.1"
__status__ = "Finished"

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



# Functions for username normalization and password generation
def normalize_username(name: str) -> str:
    name = unicodedata.normalize("NFD", name)
    name = ''.join(c for c in name if not unicodedata.combining(c))
    name = name.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    name = name.lower().replace(" ", "_")
    return ''.join(c for c in name if c.isalnum() or c == "_")

def generate_password(class_name, room_number, advisor) -> str:
    special_chars = "!%&(),._-=^#"
    random_char = random.choice(special_chars)
    return f"{class_name[0]}{random_char}{room_number[:3]}{advisor[0].upper()}"

def generate_random_password(length=12) -> str:
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!%&(),._-=^#"
    return ''.join(random.choice(chars) for _ in range(length))

# Read class data from the Excel file
try:
    class_data = pd.read_excel(args.input_file)
except FileNotFoundError:
    logger.error(f"File not found: {args.input_file}")
    exit(1)

# Prepare script contents
add_script_path = "./output/class_add.sh"
del_script_path = "./output/class_del.sh"
csv_path = "./output/class.csv"

with open(add_script_path, "w") as add_script, open(del_script_path, "w") as del_script:
    add_script.write("#!/bin/bash\n")
    del_script.write("#!/bin/bash\n")

    csv_data = []
    for _, row in (x for x in class_data.iterrows() if not pd.isnull(x[1]["Klasse"])):
        class_name = str(row["Klasse"])
        room_number = str(row["Raum Nr."])
        advisor = str(row["KV"])

        username = f"k{normalize_username(class_name)}"
        password = generate_password(class_name, room_number, advisor)

        home_dir = f"/home/klassen/{username}"
        groups = "cdrom,plugdev,sambashare"

        add_script.write(
            f"useradd -m -d {home_dir} -s /bin/bash -c '{class_name}' -G {groups} {username}\n"
            f"echo '{username}:{password}' | chpasswd\n"
        )
        del_script.write(f"userdel -r {username}\n")

        csv_data.append({"Username": username, "Password": password, "Home": home_dir})

        logger.debug(f"Created user {username} with password {password} and home directory {home_dir} for class {class_name} in room {room_number} with advisor {advisor}.")

    # Add additional users
    for user in ["lehrer", "seminar"]:
        username = user
        password = generate_random_password()
        home_dir = f"/home/lehrer/{username}"

        add_script.write(
            f"useradd -m -d {home_dir} -s /bin/bash -c '{username}' -G {groups} {username}\n"
            f"echo '{username}:{password}' | chpasswd\n"
        )
        del_script.write(f"userdel -r {username}\n")

        csv_data.append({"Username": username, "Password": password, "Home": home_dir})

