from math import gcd
from base64 import b64encode, b64decode
from Crypto.Util.number import getPrime as random_prime


'''
Helpful functions
'''


def coprimes(a_prime: int, b_prime: int) -> bool:  # Function required to find co primes numbers
    return gcd(a_prime, b_prime) == 1  # use of the function to calculate the greatest meeting of the divisor


def extended_gcd(a: int, b: int) -> (int, int, int):  # Function required to find grand common divisors of numbers
    if a == 0: return b, 0, 1  # checking the condition

    gcd, a_gcd, b_gcd = extended_gcd(b % a, a)
    return gcd, b_gcd - (b // a) * a_gcd, a_gcd


'''
Main logic of RSA cipher
'''


class RSA_Logic:  # RSA cipher logic class

    @staticmethod
    def find_d(phi: int, e: int) -> int:  # Function to find d number
        g, x, y = extended_gcd(e, phi)
        return x % phi if g == 1 else None

    @staticmethod
    def find_e(phi: int, bit: int = 16) -> int:  # Function to find e number
        while e := random_prime(bit):
            if coprimes(phi, e): return e

    @staticmethod
    def generate_keys() -> ((int, int), (int, int)):  # Function generate public and private keys of RSA cipher
        p = random_prime(8)  # random generator of prime number / 8bit
        q = random_prime(8)  # random generator of prime number / 8bit

        n = p * q  # calculation of n number
        phi = (p - 1) * (q - 1)  # calculation of phi number

        e = RSA_Logic.find_e(phi, 16)
        d = RSA_Logic.find_d(phi, e)

        return (e, n), (d, n)

    @staticmethod
    def encode(message: str, keys: (int, int)) -> str:  # Function to encode gives message
        e, n = keys

        encrypted_message = [pow(ord(c), e, n) for c in message]  # encryption of gives message / c = m^e mod n
        to_str = ' '.join([str(s) for s in encrypted_message])  # conversion message to string

        return str(b64encode(to_str.encode('utf-8')))[2:-1]  # encoding encrypted message in b64 and cutting out the
        # first 2 characters

    @staticmethod
    def decode(encrypted: str, keys: (int, int)) -> str:  # Function to decode gives message
        d, n = keys

        to_str = b64decode(encrypted).decode('utf-8')  # encryption from b64 to normal str
        numbers = [int(i) for i in to_str.split(' ')]  # convert str into a sequence of numbers

        return ''.join([chr(pow(c, d, n)) for c in numbers])  # decoding encoded message to plain text / m = c^d mod n


'''
Checking the operation of the function 
'''


if __name__ == '__main__':
    public, private = RSA_Logic.generate_keys()  # generated public and private RSA keys

    text_to_encrypt = 'To jest zakodowana wiadomość !@#$%^&*()_+1234567890-='  # plain text

    encrypted_message = RSA_Logic.encode(text_to_encrypt, public)  # encryption of gives plain text
    print(f'[{len(encrypted_message)}] {encrypted_message=}')

    decrypted_message = RSA_Logic.decode(encrypted_message, private)  # decryption of encrypted message
    print(f'[{len(decrypted_message)}] {decrypted_message=}')