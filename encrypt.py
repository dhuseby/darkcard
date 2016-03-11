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

def get_nonce(noncefile):
    return Reader.read(noncefile, joiner='')

def get_msg(msgfile):
    return Reader.read(msgfile)

def format_d8key(d8key):
    i = 0
    r = ''
    while i < len(d8key):
        row = d8key[i:i+14]
        r += ' '.join(list(row)) + '\n'
        i = i + 14
    return r

def encrypt(key, number, nonce, msg):
    box = nacl.secret.SecretBox(key, D8Key())
    if len(nonce) == 0:
        nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
    msg += "\n----\nkey # %s used on (%s):\n%s\n" % \
          (' '.join(list(number)), time.strftime("%c"), format_d8key(key))
    return "key # %s\n" % ' '.join(list(number)) + \
           nacl.encoding.HexEncoder.encode(box.encrypt(msg, nonce))
           

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print >> sys.stderr, "usage: encrypt.py <key file> <key # file> <nonce file> <msg file>"
        sys.exit(1)

    key = get_key(sys.argv[1])
    num = get_number(sys.argv[2])
    nonce = get_nonce(sys.argv[3])
    msg = get_msg(sys.argv[4])
    print >> sys.stdout, encrypt(key, num, nonce, msg)

