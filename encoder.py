class D8(object):
    """
    An 8-sided dice (D8) produces numbers 1, 2, 3, 4, 5, 6, 7, 8.  It can be
    used to generate random numbers by repeatedly rolling the dice and building
    a string of D8 digits.  This class will convert from a D8 string to binary
    and from binary to a D8 string.  D8 digits need to have 1 subtracted so
    that they fall in the range of [0-7] and for every 8 D8 digits we get 24
    bits of binary that can be converted to 3 8-bit bytes.
    """

    @staticmethod
    def encode(d):
        r = ''
        i = 0
        if len(d) % 3:
            d = '\x00' * (3 - (len(d) % 3)) + d # make it a multiple of 3 long
        while i < len(d):
            # build 24-bit value out of 8-bit bytes
            v = (ord(d[i+0]) << 16) | \
                (ord(d[i+1]) <<  8) | \
                 ord(d[i+2])
            r += chr(((v & 0xE00000) >> 21) + 49) + \
                 chr(((v & 0x1C0000) >> 18) + 49) + \
                 chr(((v & 0x038000) >> 15) + 49) + \
                 chr(((v & 0x007000) >> 12) + 49) + \
                 chr(((v & 0x000E00) >>  9) + 49) + \
                 chr(((v & 0x0001C0) >>  6) + 49) + \
                 chr(((v & 0x000038) >>  3) + 49) + \
                 chr( (v & 0x000007)        + 49)
            i = i + 3
        while r[0] == '1': # trim leading 1's
            r = r[1:]
        return r

    @staticmethod
    def decode(d):
        r = ''
        i = 0
        if len(d) & 7:
            d = '1' * (8 - (len(d) & 7)) + d # make it a multiple of 8 long
        while i < len(d):
            # build 24-bit value out of octal digits
            v = ((ord(d[i+0]) - 49) << 21) | \
                ((ord(d[i+1]) - 49) << 18) | \
                ((ord(d[i+2]) - 49) << 15) | \
                ((ord(d[i+3]) - 49) << 12) | \
                ((ord(d[i+4]) - 49) <<  9) | \
                ((ord(d[i+5]) - 49) <<  6) | \
                ((ord(d[i+6]) - 49) <<  3) | \
                 (ord(d[i+7]) - 49)
            r += chr((v & 0xFF0000) >> 16) + \
                 chr((v & 0x00FF00) >>  8) + \
                 chr( v & 0x0000FF)
            i = i + 8
        while ord(r[0]) == 0: # trim leading zeros
            r = r[1:]
        return r


class D8Key(object):
    """
    This class uses the D8 encoder to encode/decode strings of D8 rolls into
    fixed length keys for use in cryptography.
    """

    KEY_SIZE = 32 # default key size is 32 bytes (256 bits)

    def __init__(self, size=32):
        D8Key.KEY_SIZE = size

    @staticmethod
    def fixkey(d):
        """
        This function will pad a short key with leading zeros, or trim a long
        key to just the KEY_SIZE, or do nothing to a key that is the right size.
        """
        if len(d) < D8Key.KEY_SIZE:
            d = '\00' * (32 - len(d)) + d # pad with leading 0
        else:
            d = d[-32:] # trim to the 32 bytes
        return d

    @staticmethod
    def encode(d):
        return D8.encode(D8Key.fixkey(d))

    @staticmethod
    def decode(d):
        return D8Key.fixkey(D8.decode(d))

