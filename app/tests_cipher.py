from app.cipher import RSA_Logic

'''
Tests arguments
'''
text = 'To jest zakodowana wiadomość !@#$%^&*()_+1234567890-='

public, private = RSA_Logic.generate_keys()  # RSA keys generator
other_public = (50000, 47000)  # creating wrong keys
other_private = (50000, 47000)  # creating wrong keys

encoded_text = RSA_Logic.encode(text, public)  # global encoded message to use in tests
decoded_text = RSA_Logic.decode(encoded_text, private)  # global decoded message to use in tests


'''
Basic cipher unit tests
'''


def test_is_encoded():
    assert RSA_Logic.encode(text, public) == str(encoded_text)  # Tests passed when result is TRUE


def test_is_not_encoded():
    assert not RSA_Logic.encode(text, other_public) == str(encoded_text)  # Tests passed when result is FALSE


def test_is_decoded():
    assert RSA_Logic.decode(encoded_text, private) == str(decoded_text)  # Tests passed when result is TRUE


def test_is_not_decoded():
    assert not RSA_Logic.decode(encoded_text, other_private) == str(decoded_text)  # Tests passed when result is FALSE

