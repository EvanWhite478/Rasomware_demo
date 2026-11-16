
import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generate_keys(save_path):
    # Create directory if it doesn't exist
    os.makedirs(save_path, exist_ok=True)

    # Generate RSA private key
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    # Generate corresponding public key
    public_key = private_key.public_key()

    # Save private key
    private_key_path = os.path.join(save_path, "private_key.pem")
    with open(private_key_path, "wb") as f:
        f.write(private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption()))

    # Save public key
    public_key_path = os.path.join(save_path, "public_key.pem")
    with open(public_key_path, "wb") as f:
        f.write(public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo))

    print("\nKeys successfully generated!")
    print("Private key:", private_key_path)
    print("Public key:", public_key_path)


if __name__ == "__main__":
    #save_path = input("Enter directory to save keys: ")
    save_path = "C:/Users/EvanW/Desktop/Ransomware demo/Keys"
    generate_keys(save_path)
