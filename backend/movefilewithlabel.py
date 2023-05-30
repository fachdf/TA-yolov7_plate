import os
import shutil

# Specify the directory where the files are located
directory = "D:\\TUGASAKHIR\\Dataset\\DatasetMei-fix"

# Iterate over the files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".jpg"):
        # Get the corresponding TXT file name
        txt_filename = os.path.splitext(filename)[0] + ".txt"
        txt_filepath = os.path.join(directory, txt_filename)
        
        # Check if the corresponding TXT file exists
        if os.path.exists(txt_filepath):
            # Move the JPG file to a new directory
            destination_directory = "D:/TUGASAKHIR/Dataset/DatasetMei-fix/fix"
            destination_filepath = os.path.join(destination_directory, filename)
            shutil.move(os.path.join(directory, filename), destination_filepath)
            shutil.move(os.path.join(directory, txt_filename), destination_filepath)
            print(f"Moved {filename} to {destination_directory}")
        else:
            print(f"No corresponding TXT file found for {filename}")