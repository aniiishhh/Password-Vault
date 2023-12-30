from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64


def generate_key_from_passphrase(passphrase):
    # Convert passphrase to bytes
    passphrase_bytes = passphrase.encode("utf-8")

    # Generate a salt using a cryptographically secure random number generator
    salt = Fernet.generate_key()

    # Create a PBKDF2HMAC instance with the desired parameters
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=salt,
        iterations=100000,  # Number of iterations for key stretching
        length=32,  # Length of the derived key
    )

    # Derive the key from the passphrase
    key = kdf.derive(passphrase_bytes)
    encoded_key = base64.urlsafe_b64encode(key)
    encoded_salt = base64.urlsafe_b64encode(salt)
    return (encoded_key, encoded_salt)


def generate_specific_key_from_passphrase(passphrase, encoded_salt):
    # Convert passphrase to bytes
    passphrase_bytes = passphrase.encode("utf-8")

    # Decode the encoded salt
    salt = base64.urlsafe_b64decode(encoded_salt)

    # Create a PBKDF2HMAC instance with the desired parameters
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=salt,
        iterations=100000,  # Number of iterations for key stretching
        length=32,  # Length of the derived key
    )

    # Derive the key from the passphrase
    key = kdf.derive(passphrase_bytes)

    encoded_key = base64.urlsafe_b64encode(key)
    return encoded_key


# Function to encrypt data using a provided key
def encrypt_data(data, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode("utf-8"))
    return encrypted_data


# Function to decrypt data using a provided key
def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data.decode("utf-8")


# passphrase = "AnishDEMO1#*"
# tuple_pass = generate_key_from_passphrase(passphrase)
# encoded_password = tuple_pass[0]
# salt = tuple_pass[1]

# print(encoded_password)
# print(generate_specific_key_from_passphrase(passphrase, salt))
