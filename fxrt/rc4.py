import binascii

# Global variables
state = [None] * 256
p = q = None


def setKey(key):
    ##RC4 Key Scheduling Algorithm (KSA)
    global p, q, state
    state = [n for n in range(256)]
    p = q = j = 0
    for i in range(256):
        if len(key) > 0:
            j = (j + state[i] + key[i % len(key)]) % 256
        else:
            j = (j + state[i]) % 256
        state[i], state[j] = state[j], state[i]


def byteGenerator():
    ##RC4 Pseudo-Random Generation Algorithm (PRGA)
    global p, q, state
    p = (p + 1) % 256
    q = (q + state[p]) % 256
    state[p], state[q] = state[q], state[p]
    return state[(state[p] + state[q]) % 256]


def encrypt(key, plaintext):
    ##Encrypt input string returning a byte list
    pt = string_to_list(plaintext)
    ct = rc4(key, pt)
    return list_to_string(ct, hex=True)


def decrypt(key, ciphertext):
    ##Decrypt input byte list returning a string
    ct = string_to_list(ciphertext, hex=True)
    pt = rc4(key, ct)
    return list_to_string(pt, hex=False)


def string_to_list(input_srt, hex=False):
    ##Convert a string into an int list
    if hex:
        res = [ch for ch in binascii.unhexlify(input_srt)]
    else:
        res = [ord(ch) for ch in input_srt]
    return res


def list_to_string(lst, hex=True):
    ##Convert an int list into a string
    if hex:
        res = ''.join(["%0.2X" % el for el in lst])
    else:
        res = ''.join([chr(el) for el in lst])
    return res


def rc4(key, ints):
    """Xor list of ints with output generated by RC4. Output list of ints"""
    setKey(string_to_list(key))
    return [x ^ byteGenerator() for x in ints]