# 2025.11.20 Data Calculating templet
import binascii


# 2025.11.17: Convert a protocol command to byte
def to_bytes_payload(value) -> bytes:
    """
    Accept bytes, bytearray, a list/tuple of ints, or a hex string.
    Examples: b'\\xff\\x00...', [0xff, 0x00, 0x21], 'ff 00 21', 'ff,00,21'
    """
    if isinstance(value, (bytes, bytearray)):
        return bytes(value)

    if isinstance(value, (list, tuple)):
        # Clamp each integer to a single byte.
        return bytes(int(x) & 0xFF for x in value)

    if isinstance(value, str):
        s = value.strip().lower()
        # Normalize separators.
        s = s.replace(',', ' ').replace('0x', '')
        # Remove spaces and pad odd-length input if needed.
        hexchars = ''.join(s.split())
        if len(hexchars) % 2 != 0:
            # Handle a leading single nibble such as 'f 00 ...'.
            hexchars = '0' + hexchars
        try:
            return binascii.unhexlify(hexchars)
        except binascii.Error:
            # Fall back to token-by-token parsing for mixed-width input.
            parts = [p for p in s.split() if p]
            return bytes(int(p, 16) & 0xFF for p in parts)

    raise TypeError("Unsupported payload type for byte conversion")
