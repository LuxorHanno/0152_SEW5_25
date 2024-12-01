__author__ = "Hanno Postl"
__version__ = "1.3"
__status__ = "Finished"

import pandas as pd
import unicodedata
import random
import os
import logging
import argparse
from logging.handlers import RotatingFileHandler
from typing import Dict, List

# Argument parser setup
parser = argparse.ArgumentParser(description="Create user accounts from an Excel file.")
parser.add_argument("input_file", help="Path to the input Excel file")
parser.add_argument("-o", "--output", choices=["csv", "xlsx"], default="csv", help="Output format: csv or xlsx")
parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
parser.add_argument("-q", "--quiet", action="store_true", help="Enable quiet logging")
args = parser.parse_args()

# Logging configuration
log_file: str = "./output/create_user.log"
os.makedirs("./output", exist_ok=True)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG if args.verbose else logging.WARNING if args.quiet else logging.INFO)

handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=5)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)

def normalize_username(name: str) -> str:
    """
    Normalize a username by replacing German umlauts, converting to lowercase,
    removing accents, and keeping only alphanumeric characters and underscores.

    Parameters:
    name (str): The original username.

    Returns:
    str: The normalized username.
    """
    name = unicodedata.normalize("NFD", name)
    name = ''.join(c for c in name if not unicodedata.combining(c))
    name = name.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    name = name.lower().replace(" ", "_")
    return ''.join(c for c in name if c.isalnum() or c == "_")

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

# Read user data from the Excel file
try:
    user_data: pd.DataFrame = pd.read_excel(args.input_file)
except FileNotFoundError:
    logger.error(f"File not found: {args.input_file}")
    exit(1)

# Prepare script contents
add_script_path: str = "./output/user_add.sh"
output_path: str = f"./output/user.{args.output}"

usernames: Dict[str, int] = {}
with open(add_script_path, "w") as add_script:
    add_script.write("#!/bin/bash\n")

    csv_data: List[Dict[str, str]] = []
    for _, row in user_data.iterrows():
        last_name: str = str(row["lastname"])
        groups: str = str(row["group"]) + ",cdrom,plugdev,sambashare," + str(row["class"])
        username: str = normalize_username(last_name)

        # Handle duplicate usernames
        if username in usernames:
            count: int = usernames[username] + 1
            usernames[username] = count
            username = f"{username}{count}"
        else:
            usernames[username] = 0

        password: str = generate_random_password()
        home_dir: str = f"/home/{username}"

        add_script.write(
            f"useradd -m -d {home_dir} -s /bin/bash -c '{last_name}' -G {groups} {username}\n"
            f"echo '{username}:{password}' | chpasswd\n"
        )

        csv_data.append({"Username": username, "Password": password, "Home": home_dir})

        logger.debug(f"Created user {username} with password {password} and home directory {home_dir} for last name {last_name}.")

# Save output
csv_df: pd.DataFrame = pd.DataFrame(csv_data)
if args.output == "csv":
    csv_df.to_csv(output_path, index=False)
else:
    csv_df.to_excel(output_path, index=False)

logger.info(f"Script user_add.sh and user.{args.output} successfully created.")