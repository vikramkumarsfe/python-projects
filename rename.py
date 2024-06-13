import os

def rename_png_files(folder_path):
    try:
        # Get a list of all files in the folder
        files = os.listdir(folder_path)
        png_files = [file for file in files if file.endswith(".png")]

        # Sort the PNG files alphabetically
        png_files.sort()

        # Iterate through the PNG files and rename them in numerical order
        for i, file in enumerate(png_files, start=28):
            # Construct the new file name
            new_file_name = f"{i}.png"

            # Rename the file
            old_file_path = os.path.join(folder_path, file)
            new_file_path = os.path.join(folder_path, new_file_name)
            os.rename(old_file_path, new_file_path)

            print(f"File renamed: {file} -> {new_file_name}")

    except Exception as e:
        print(f"Error renaming files: {e}")

# Example usage
if __name__ == "__main__":
    folder_path = "C:\\Users\\vikra\\Desktop\\meet-up web\\output"  # Replace with the path to your folder containing PNG files
    rename_png_files(folder_path)
