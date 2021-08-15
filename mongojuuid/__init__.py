import itertools
import re

# reference: https://gist.github.com/davideicardi/b0228fbc0d2e0a65bfc0f70a3cb8d9cf

BASE64_DIGITS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
HEX_DIGITS = "0123456789abcdef"


def to_bindata(*uuids):
    """
    Converts given UUIDs to (old) BinData formats like the Java Mongo Driver would do.
    This means the bytes will be reordered.
    See also https://jira.mongodb.org/browse/JAVA-403
    """
    bindatas = []
    for uuid in uuids:
        _hex = _java_hex(uuid)
        base64 = _to_base64(_hex)
        bindatas.append(f'BinData(3, "{base64}")')
    return bindatas


def to_uuid(*bindatas):
    """
    Converts (old) BinData formats back to UUIDs like the Java Mongo Driver would do.
    This means the bytes will be reordered.
    See also https://jira.mongodb.org/browse/JAVA-403
    """
    uuids = []
    for bindata in bindatas:
        _hex = _to_hex(bindata)
        _hex = _java_hex(_hex)
        uuid = f'{_hex[0:8]}-{_hex[8:12]}-{_hex[12:16]}-{_hex[16:20]}-{_hex[20:32]}'
        uuids.append(uuid)
    return uuids


def _to_base64(_hex):
    _hex = re.sub(r'[{}-]', '', _hex)
    base64 = ''
    # uuid -> 32 hex digits -> 16 bytes -> 128bits
    # get groups of 6 hex digits (total 5, remaining 2)
    # 6 hex digits will be mapped to 4 base64 digits (6 hex = 4*6 bits = 4 * index_base64)
    groups = [_hex[i:i + 6] for i in range(0, 30, 6)]
    for group in groups:
        n = int(f'0x{group}', base=16)
        # each two hex digits consume 1 byte => 6 hex digits = 24 bits
        # get for each group of 6 bits the base64 char (why 6? because 0x3f = 64 = number of base64 digits)
        # to do so, shift the each group as far as possible to the right and crop to 6 bits
        # build the index from the 6 bits and get the char
        base64 += BASE64_DIGITS[(n >> 18) & 0x3f]
        base64 += BASE64_DIGITS[(n >> 12) & 0x3f]
        base64 += BASE64_DIGITS[(n >> 6) & 0x3f]
        # no need to shift just apply bitmask to get the last 6 bits
        base64 += BASE64_DIGITS[n & 0x3f]
    # last two hex digits => 8 bits
    n = int(f'0x{_hex[30:32]}', base=16)
    # convert the first 6 bits
    base64 += BASE64_DIGITS[(n >> 2) & 0x3f]
    # convert the last two bits to base64 digits by shifting to the left by 4 bits (??0000)
    # allows us to use the same 6 bit bitmask
    index = (n << 4) & 0x3f
    base64 += BASE64_DIGITS[index]
    base64 += '=='
    return base64


def _to_hex(bindata):
    base64 = re.sub(r'BinData\(3,["\']([^\)]+)["\']\)', '\\1', bindata).strip()
    groups = [base64[i:i + 4] for i in range(0, 24, 4)]
    _hex = ""
    for group in groups:
        e1 = BASE64_DIGITS.index(group[0])
        e2 = BASE64_DIGITS.index(group[1])
        e3 = BASE64_DIGITS.index(group[2])
        e4 = BASE64_DIGITS.index(group[3])
        # 6 hex digits were mapped to 4 base64 chars, each base64 char takes 6 bits
        # here we go through a sliding window of 8 bits using the bitwise or operator
        # thus, each chunk consists of 2 hex digits (1 hex digit = 4 bits)
        c1 = (e1 << 2) | (e2 >> 4)
        c2 = ((e2 & 15) << 4) | (e3 >> 2)
        c3 = ((e3 & 3) << 6) | e4
        _hex += HEX_DIGITS[c1 >> 4]  # get first digit (msb) by shifting to the left by 4 bits
        _hex += HEX_DIGITS[c1 & 15]  # get second digit (lsb) by applying 15 as netmask 0b1111
        if e3 != 64: # not equal sign
            _hex += HEX_DIGITS[c2 >> 4]
            _hex += HEX_DIGITS[c2 & 15]
        if e4 != 64:
            _hex += HEX_DIGITS[c3 >> 4]
            _hex += HEX_DIGITS[c3 & 15]
    return _hex


def _java_hex(uuid):
    """Java Mongo Driver transfers byte representation of UUIDs in little endian format.
    See also https://jira.mongodb.org/browse/JAVA-403
    :param uuid:
    :return: reordered hex sequence
    """
    _hex = re.sub(r'[{}-]', '', uuid)
    bytes = list(zip(_hex[0::2], _hex[1::2]))
    msb = "".join(itertools.chain(*bytes[0:8][::-1]))
    lsb = "".join(itertools.chain(*bytes[8:16][::-1]))
    _hex = msb + lsb
    return _hex


__all__ = [to_uuid.__name__, to_bindata.__name__]
