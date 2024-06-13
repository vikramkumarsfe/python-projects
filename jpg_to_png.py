from PIL import Image
import os

def convert_jpg_to_png(input_folder, output_folder):
    try:
        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Iterate through all files in the input folder
        for filename in os.listdir(input_folder):
            if filename.endswith(".jpg"):
                input_path = os.path.join(input_folder, filename)
                output_path = os.path.join(output_folder, filename[:-4] + ".png")  # Change file extension to PNG

                # Open the JPG image
                with Image.open(input_path) as img:
                    # Convert the image to RGBA mode to support transparency
                    img = img.convert("RGBA")
                    # Save the image as PNG
                    img.save(output_path, "PNG")
                print(f"Image converted successfully: {output_path}")
    except Exception as e:
        print(f"Error converting image: {e}")

# Example usage
if __name__ == "__main__":
    input_folder = f'C:\\Users\\vikra\\Desktop\\meet-up web'  # Replace with the path to your input folder containing JPG images
    output_folder = f'C:\\Users\\vikra\\Desktop\\meet-up web\\output'  # Replace with the path to the output folder for PNG images
    convert_jpg_to_png(input_folder, output_folder)
