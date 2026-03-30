import sys

from file_scan.scanner import FileSignatureScanner


# Personal note:
# Simple command line interface.
# Later I may add directory scanning and JSON output.


def main():

    # Check if a file argument was provided
    if len(sys.argv) < 2:
        print("Usage: python cli.py <file>")
        return

    file_path = sys.argv[1]

    scanner = FileSignatureScanner()

    results = scanner.scan(file_path)

    # No match found
    if not results:
        print("Unknown file type")
        return

    # Print all matching signatures
    for result in results:

        print("Match Found")
        print("Description:", result["description"])
        print("Class:", result["class"])

        if result["extensions"]:
            print("Possible Extensions:", ", ".join(result["extensions"]))

        print("-" * 40)


if __name__ == "__main__":
    main()