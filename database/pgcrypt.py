import base64
import binascii
import unittest

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

def encrypt_string(plaintext: str, key: str) -> str:
    """
    Encrypts a string using AES-GCM with the provided key.

    Args:
        plaintext (str): The string to encrypt.
        key (str): The encryption key (must be at least 32 characters).

    Returns:
        str: The encrypted string, base64-encoded.

    Raises:
        ValueError: If the key is None or less than 32 characters.
    """
    if key is None or len(key) < 32:
        raise ValueError("Encryption key must be at least 32 characters long")

    key_bytes = key.encode('utf-8')

    iv = os.urandom(12)

    cipher = Cipher(algorithms.AES(key_bytes), modes.GCM(iv))
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(plaintext.encode('utf-8')) + encryptor.finalize()
    encrypted_data = iv + ciphertext + encryptor.tag

    return base64.b64encode(encrypted_data).decode('utf-8')

def decrypt_string(ciphertext: str, key: str) -> str:
    """
    Decrypts a string that was encrypted using AES-GCM with the provided key.

    Args:
        ciphertext (str): The encrypted string, base64-encoded.
        key (str): The decryption key (must be at least 32 characters).

    Returns:
        str: The decrypted string.

    Raises:
        ValueError: If the key is None or less than 32 characters.
    """
    if key is None or len(key) < 32:
        raise ValueError("Decryption key must be at least 32 characters long")

    key_bytes = key.encode('utf-8')

    encrypted_data = base64.b64decode(ciphertext)

    iv = encrypted_data[:12]
    ciphertext = encrypted_data[12:-16]
    tag = encrypted_data[-16:]

    cipher = Cipher(algorithms.AES(key_bytes), modes.GCM(iv, tag))
    decryptor = cipher.decryptor()

    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    return plaintext.decode('utf-8')

class TestEncryptionDecryption(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.key_32 = binascii.hexlify(os.urandom(16)).decode()
        cls.key_64 = binascii.hexlify(os.urandom(32)).decode()

    def test_encrypt_decrypt(self):
        plaintext = "This is a test message."
        encrypted = encrypt_string(plaintext, self.key_32)
        decrypted = decrypt_string(encrypted, self.key_32)
        self.assertEqual(plaintext, decrypted)

    def test_long_message(self):
        plaintext = "Abcdefg" * 1000
        encrypted = encrypt_string(plaintext, self.key_32)
        decrypted = decrypt_string(encrypted, self.key_32)
        self.assertEqual(plaintext, decrypted)

    def test_special_characters(self):
        plaintext = "!@#$%^&*()_+{}[]|\\:;\"'<>,.?/~`"
        encrypted = encrypt_string(plaintext, self.key_32)
        decrypted = decrypt_string(encrypted, self.key_32)
        self.assertEqual(plaintext, decrypted)

    def test_unicode_characters(self):
        plaintext = "Hello, 世界! こんにちは! Здравствуй! 🌍🌎🌏"
        encrypted = encrypt_string(plaintext, self.key_32)
        decrypted = decrypt_string(encrypted, self.key_32)
        self.assertEqual(plaintext, decrypted)

    def test_multiple_calls_produce_different_ciphertexts(self):
        plaintext = "Same plaintext, same key"
        encrypted1 = encrypt_string(plaintext, self.key_32)
        encrypted2 = encrypt_string(plaintext, self.key_32)
        self.assertNotEqual(encrypted1, encrypted2)

    def test_short_key(self):
        plaintext = "This shouldn't work"
        with self.assertRaises(ValueError):
            encrypt_string(plaintext, "shorty")

    def test_none_key(self):
        plaintext = "This shouldn't work"
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            encrypt_string(plaintext, None)

    def test_empty_string(self):
        plaintext = ""
        encrypted = encrypt_string(plaintext, self.key_32)
        decrypted = decrypt_string(encrypted, self.key_32)
        self.assertEqual(plaintext, decrypted)

    def test_incorrect_key_for_decryption(self):
        plaintext = "This message will be decrypted with the wrong key"
        encrypted = encrypt_string(plaintext, self.key_32)
        with self.assertRaises(Exception):
            decrypt_string(encrypted, self.key_64)

    def test_tampered_ciphertext(self):
        plaintext = "This ciphertext will be tampered with"
        encrypted = encrypt_string(plaintext, self.key_32)
        tampered = base64.b64encode(base64.b64decode(encrypted)[:-1] + b'X').decode()
        with self.assertRaises(Exception):
            decrypt_string(tampered, self.key_32)

if(__name__ == "__main__"):
    unittest.main()