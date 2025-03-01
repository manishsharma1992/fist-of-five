from cryptography.fernet import Fernet

def generate_encryption_key() -> str:
    """
    Generates a URL-safe base64-encoded 32-byte key.
    """
    key = Fernet.generate_key()
    return key.decode('utf-8')

def encrypt_password(plain_password: str, encryption_key: str) -> str:
    """
    Encrypts the provided plain text password using the given encryption key.
    Returns the encrypted password as a string.
    """
    fernet = Fernet(encryption_key.encode('utf-8'))
    encrypted_password = fernet.encrypt(plain_password.encode('utf-8'))
    return encrypted_password.decode('utf-8')

if __name__ == "__main__":
    # Generate an encryption key (store this key securely)
    key = generate_encryption_key()
    print("Encryption Key:", key)

    # Encrypt a sample password
    password_to_encrypt = ""
    encrypted = encrypt_password(password_to_encrypt, key)
    print("Encrypted Password:", encrypted)
