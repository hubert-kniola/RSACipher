from cipher import RSA_Logic
import pytest


def is_encoded(message: str, public, encoded_text) -> bool:
    return RSA_Logic.encode_v2(message, public) == str(encoded_text)


def is_decoded(message: str, private, decoded_text) -> bool:
    return RSA_Logic.decode_v2(message, private) == str(decoded_text)


class test_class:

    def test_is_encoded(message: str, public, encoded):
        assert is_encoded(message, public, encoded)

    def test_is_not_encoded(message: str, public, encoded):
        assert not is_encoded(message, public, encoded), 'Message cannot be encoded'

    def test_is_decoded(message: str, private, decoded):
        assert is_decoded(message, private, decoded)

    def test_is_not_decoded(message: str, private, decoded):
        assert not is_decoded(message, private, decoded), 'Message cannot be decoded'


text = 'To jest zakodowana wiadomość !@#$%^&*()_+1234567890-='

public, private = RSA_Logic.generate_keys()
print(public, private)
other_public = (50000, 47000)
other_private = (50000, 47000)

encoded_text = RSA_Logic.encode_v2(text, public)
decoded_text = RSA_Logic.decode_v2(encoded_text, private)

print(encoded_text)
print(decoded_text)

test_class.test_is_encoded(text, public, encoded_text)
test_class.test_is_not_encoded(text, other_public, encoded_text)
test_class.test_is_decoded(text, private, decoded_text)
test_class.test_is_not_decoded(text, other_private, decoded_text)

