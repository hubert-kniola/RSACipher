from math import gcd
from base64 import b64encode, b64decode
from Crypto.Util.number import getPrime as random_prime


def coprimes(a_prime: int, b_prime: int) -> bool:
    return gcd(a_prime, b_prime) == 1


def extended_gcd(a: int, b: int) -> (int, int, int):
    if a == 0: return b, 0, 1

    gcd, a_gcd, b_gcd = extended_gcd(b % a, a)
    return gcd, b_gcd - (b // a) * a_gcd, a_gcd


class RSA_Logic:

    @staticmethod
    def find_d(phi: int, e: int) -> int:
        g, x, y = extended_gcd(e, phi)
        return x % phi if g == 1 else None

    @staticmethod
    def find_e(phi: int, bit: int = 16) -> int:
        while e := random_prime(bit):
            if coprimes(phi, e): return e

    @staticmethod
    def generate_keys() -> ((int, int), (int, int)):
        p = random_prime(8)
        q = random_prime(8)

        n = p * q
        phi = (p - 1) * (q - 1)

        e = RSA_Logic.find_e(phi, 16)
        d = RSA_Logic.find_d(phi, e)

        return (e, n), (d, n)

    @staticmethod
    def encode(message: str, keys: (int, int)) -> bytes:

        e, n = keys

        encrypted_message = [pow(ord(c), e, n) for c in message]
        to_str = ' '.join([str(s) for s in encrypted_message])

        return b64encode(to_str.encode('utf-8'))

    @staticmethod
    def decode(encrypted: bytes, keys: (int, int)) -> str:
        d, n = keys

        to_str = b64decode(encrypted).decode('utf-8')
        numbers = [int(i) for i in to_str.split(' ')]

        return ''.join([chr(pow(c, d, n)) for c in numbers])

    @staticmethod
    def encode_v2(message: str, keys: (int, int)) -> str:
        e, n = keys

        encrypted_message = [pow(ord(c), e, n) for c in message]
        #print(encrypted_message)
        to_str = ' '.join([str(s) for s in encrypted_message])
        #print(to_str)

        return to_str

    @staticmethod
    def decode_v2(encrypted: str, keys: (int, int)) -> str:
        d, n = keys

        to_str = encrypted
        numbers = [int(i) for i in to_str.split(' ')]

        return ''.join([chr(pow(c, d, n)) for c in numbers])


if __name__ == '__main__':
    #RSA_Logic.test()
    public, private = RSA_Logic.generate_keys()

    text_to_encrypt = 'To jest zakodowana wiadomość !@#$%^&*()_+1234567890-='

    encrypted_message = RSA_Logic.encode(text_to_encrypt, public)
    print(f'[{len(encrypted_message)}] {encrypted_message=}')

    decrypted_message = RSA_Logic.decode(encrypted_message, private)
    print(f'[{len(decrypted_message)}] {decrypted_message=}')

    # Check for tests

    encrypted_message = RSA_Logic.encode_to_test(text_to_encrypt, public)
    print(f'[{len(encrypted_message)}] {encrypted_message=}')

    decrypted_message = RSA_Logic.decode_to_test(encrypted_message, private)
    print(f'[{len(decrypted_message)}] {decrypted_message=}')
