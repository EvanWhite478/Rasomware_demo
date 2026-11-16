
import os
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def decrypt_folder(folder_path, private_key_path):
    folder = Path(folder_path)

    # Remove "_Encrypted" from folder name
    output_folder = folder.parent / folder.name.replace("_Encrypted", "_Decrypted")

    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)

    # Create output directory
    output_folder.mkdir(parents=True, exist_ok=True)

    # Walk through encrypted folder
    for root, dirs, files in os.walk(folder):
        relative_path = Path(root).relative_to(folder)
        decrypted_dir = output_folder / relative_path
        decrypted_dir.mkdir(parents=True, exist_ok=True)

        for filename in files:
            if not filename.endswith(".enc"):
                continue
            encrypted_path = Path(root) / filename
            # Read encrypted file
            with open(encrypted_path, "rb") as file:
                encrypted_key_length = int.from_bytes(file.read(2), "big")

                encrypted_key = file.read(encrypted_key_length)
                nonce = file.read(12)
                encrypted_data = file.read()

            # Decrypt AES key using RSA private key
            aes_key = private_key.decrypt(encrypted_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

            # Decrypt file using AES-GCM
            aesgcm = AESGCM(aes_key)
            decrypted_data = aesgcm.decrypt(nonce, encrypted_data, None)

            # Remove .enc extension
            original_filename = filename[:-4]
            output_path = decrypted_dir / original_filename

            # Save decrypted file
            with open(output_path, "wb") as output_file:
                output_file.write(decrypted_data)

    print("Folder decryption complete!")
    print("Decrypted folder:", output_folder)


if __name__ == "__main__":

    #folder = input("Enter encrypted folder path: ")
    folder = "C:/Users/EvanW/Desktop/Ransomware demo/Output/Payroll_Encrypted"
    #private_key = input("Enter private key path: ")
    private_key = "C:/Users/EvanW/Desktop/Ransomware demo/Output/Keys/private_key.pem"

    try:
        decrypt_folder(folder, private_key)

    except Exception as error:
        print("Decryption failed:", error)
