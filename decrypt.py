from encoder import D8Key
from util import Reader
import nacl.secret
import nacl.utils
import nacl.encoding
import sys, time

def get_key(keyfile):
    return Reader.read(keyfile, joiner='')

def get_number(numfile):
    return Reader.read(numfile, joiner='')

def decrypt(key, num, msgfile):
    if len(key) == 0:
        print >> sys.stderr, "invalid key length, aborting."
        sys.exit(1)

    with open(msgfile, 'r') as f:
        lines = f.readlines()

    if ' '.join(list(num)) != lines[0][6:].strip('\n\r'):
        print >> sys.stderr, "key # mismatch, you're probably using the wrong key."

    msg = nacl.encoding.HexEncoder.decode(lines[1].strip('\n\r'))
    box = nacl.secret.SecretBox(key, D8Key())
    return box.decrypt(msg)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print >> sys.stderr, "usage: decrypt.py <key file> <key # file> <msg file>"
        sys.exit(1)

    key = get_key(sys.argv[1])
    num = get_number(sys.argv[2])
    print >> sys.stdout, decrypt(key, num, sys.argv[3])

