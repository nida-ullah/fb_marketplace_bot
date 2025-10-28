"""
Password encryption utilities for Facebook account passwords.
Uses Fernet (symmetric encryption) to securely store passwords.
"""

from cryptography.fernet import Fernet
from django.conf import settings


class PasswordEncryption:
    """
    Encrypt and decrypt Facebook passwords using Fernet encryption.
    """

    @staticmethod
    def get_cipher():
        """Get encryption cipher from settings"""
        key = settings.FACEBOOK_PASSWORD_ENCRYPTION_KEY.encode()
        return Fernet(key)

    @staticmethod
    def encrypt(password):
        """
        Encrypt a plain text password.

        Args:
            password (str): Plain text password

        Returns:
            str: Encrypted password (base64 encoded)
        """
        if not password:
            return None
        cipher = PasswordEncryption.get_cipher()
        encrypted = cipher.encrypt(password.encode())
        return encrypted.decode()

    @staticmethod
    def decrypt(encrypted_password):
        """
        Decrypt an encrypted password.

        Args:
            encrypted_password (str): Encrypted password (base64 encoded)

        Returns:
            str: Decrypted plain text password
        """
        if not encrypted_password:
            return None
        cipher = PasswordEncryption.get_cipher()
        decrypted = cipher.decrypt(encrypted_password.encode())
        return decrypted.decode()
