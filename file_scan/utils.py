# Utility helpers used by the scanner
# Notes to self: keep anything related to data cleanup here so scanner.py stays simple


def clean_hex(hex_string):
    """
    Convert the hex signature string from the database into bytes.
    Example: "00 00 01 B3" -> b'\x00\x00\x01\xb3'
    """

    # Some entries in the database contain "(null)"
    # These cannot be converted into signatures
    if hex_string == "(null)" or not hex_string:
        return None

    # The JSON stores hex values separated by spaces
    # Remove spaces before converting
    hex_string = hex_string.replace(" ", "")

    return bytes.fromhex(hex_string)


def parse_extensions(extension_string):
    """
    Convert extension field into a list.

    Example:
    "MP4|M4V|3GP" -> ["MP4","M4V","3GP"]
    """

    if extension_string in ("(none)", "", None):
        return []

    # Multiple extensions are separated with "|"
    return extension_string.split("|")