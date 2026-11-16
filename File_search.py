
import os

def find_folder(directory, keyword):
    # Walk through the directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        for folder in dirs:
            if folder.lower() == keyword.lower():
                return os.path.join(root, folder)

    return None


# Get user input
#directory = input("Enter the directory to search: ")
directory = "C:/Users/EvanW/Desktop/Ransomware demo/Target"
#keyword = input("Enter the folder name to find: ")
keyword = "Payroll"

# Search for the folder
result = find_folder(directory, keyword)

# Display the result
if result:
    print("\nFolder found!")
    print("Folder path:", result)
else:
    print("\nFolder not found.")
