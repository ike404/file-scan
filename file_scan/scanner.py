import json
import os

from .utils import clean_hex, parse_extensions


# Personal note:
# This is the core engine.
# It loads the signature database once and stores all signatures in memory.


class FileSignatureScanner:

    def __init__(self, db_path=None):

        # Determine path to signature database
        # Using relative path so the program works regardless of where it is run

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        if db_path is None:
            db_path = os.path.join(base_dir, "data", "file_sigs.json")

        # Load JSON database
        with open(db_path, "r") as f:
            data = json.load(f)

        self.signatures = []

        # Parse every signature entry into a faster internal format
        for entry in data["filesigs"]:

            header = clean_hex(entry["Header (hex)"])
            trailer = clean_hex(entry["Trailer (hex)"])

            offset = int(entry["Header offset"])

            self.signatures.append({
                "description": entry["File description"],
                "extensions": parse_extensions(entry["File extension"]),
                "class": entry["FileClass"],
                "header": header,
                "trailer": trailer,
                "offset": offset
            })

    def scan(self, file_path):

        # Read first part of the file
        # Most signatures appear in the first few hundred bytes
        with open(file_path, "rb") as f:
            data = f.read(4096)

        matches = []

        # Check file against every known signature
        for sig in self.signatures:

            header = sig["header"]

            # Skip entries without a usable header
            if header is None:
                continue

            offset = sig["offset"]

            start = offset
            end = offset + len(header)

            # Compare bytes directly
            if data[start:end] == header:
                matches.append(sig)

        return matches