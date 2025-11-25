# 2025.11.20 Data Calculating templet
import binascii


# 2025.11.17: Convert a protocol command to byte
def to_bytes_payload(value) -> bytes:
    """
    value: bytes | bytearray | list[int] | tuple[int] | str(공백/쉼표 포함 hex) 모두 허용.
    예) b'\xff\x00...', [0xff,0x00,0x21], 'ff 00 21 13 00 01 35', 'ff,00,21,13,00,01,35'
    """
    if isinstance(value, (bytes, bytearray)):
        return bytes(value)

    if isinstance(value, (list, tuple)):
        # 정수 범위 검증
        return bytes(int(x) & 0xFF for x in value)

    if isinstance(value, str):
        s = value.strip().lower()
        # 구분자 통일
        s = s.replace(',', ' ').replace('0x', '')
        # 공백 제거 후 짝수 길이가 아니면 보정
        hexchars = ''.join(s.split())
        if len(hexchars) % 2 != 0:
            # 'f 00 ...' 처럼 홀수 nibble 방지
            hexchars = '0' + hexchars
        try:
            return binascii.unhexlify(hexchars)
        except binascii.Error:
            # 공백 단위로 나눠서 바이트화 (예: "ff 0 21" 같은 케이스)
            parts = [p for p in s.split() if p]
            return bytes(int(p, 16) & 0xFF for p in parts)

    raise TypeError("Unsupported type for payload -> bytes 변환 실패")
