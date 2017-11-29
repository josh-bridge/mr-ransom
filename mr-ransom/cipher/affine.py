# Affine Cipher
# http://inventwithpython.com/hacking (BSD Licensed)

import sys

from script.cipher import cryptomath

SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='  # note the space at the front


class AffineCipher:
    def __init__(self, key):
        self.key = key

    def process(self, message, mode):
        if mode == 'encrypt':
            return encrypt_message(self.key, message)
        elif mode == 'decrypt':
            return decrypt_message(self.key, message)


def get_key_parts(key):
    key_a = key // len(SYMBOLS)
    key_b = key % len(SYMBOLS)
    return key_a, key_b


def check_keys(key_a, key_b, mode):
    if key_a == 1 and mode == 'encrypt':
        sys.exit('The affine cipher becomes incredibly weak when key A is set to 1. Choose a different key.')
    if key_b == 0 and mode == 'encrypt':
        sys.exit('The affine cipher becomes incredibly weak when key B is set to 0. Choose a different key.')
    if key_a < 0 or key_b < 0 or key_b > len(SYMBOLS) - 1:
        sys.exit('Key A must be greater than 0 and Key B must be between 0 and %s.' % (len(SYMBOLS) - 1))
    if cryptomath.gcd(key_a, len(SYMBOLS)) != 1:
        sys.exit('Key A (%s) and the symbol set size (%s) are not relatively prime. Choose a different key.' % (key_a, len(SYMBOLS)))


def encrypt_message(key, message):
    key_a, key_b = get_key_parts(key)
    check_keys(key_a, key_b, 'encrypt')
    cipher_text = ''
    for symbol in message:
        if symbol in SYMBOLS:
            # encrypt this symbol
            sym_index = SYMBOLS.find(symbol)
            cipher_text += SYMBOLS[(sym_index * key_a + key_b) % len(SYMBOLS)]
        else:
            cipher_text += symbol  # just append this symbol un-encrypted
    return cipher_text


def decrypt_message(key, message):
    key_a, key_b = get_key_parts(key)
    check_keys(key_a, key_b, 'decrypt')
    plaintext = ''
    mod_inverse_of_key_a = cryptomath.find_mod_inverse(key_a, len(SYMBOLS))

    for symbol in message:
        if symbol in SYMBOLS:
            # decrypt this symbol
            sym_index = SYMBOLS.find(symbol)
            plaintext += SYMBOLS[(sym_index - key_b) * mod_inverse_of_key_a % len(SYMBOLS)]
        else:
            plaintext += symbol  # just append this symbol un-decrypted
    return plaintext