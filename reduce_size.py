import os
from PIL import Image


def compress_image(input_path, output_path, max_size_kb=900):
    img = Image.open(input_path)
    if img.mode in ("RGBA", "P"):  # Convert to RGB if necessary
        img = img.convert("RGB")

    quality = 85  # Start with high quality
    img.save(output_path, 'JPEG', quality=quality)

    # Reduce quality until the file size is under the max_size_kb
    while os.path.getsize(output_path) > max_size_kb * 1024 and quality > 10:
        quality -= 5
        img.save(output_path, 'JPEG', quality=quality)
        print(f"Reducing quality to {quality} for {output_path}")


def compress_images_in_folder(source_folder, destination_folder, max_size_kb=900):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for filename in os.listdir(source_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(source_folder, filename)
            output_path = os.path.join(destination_folder, filename)
            compress_image(input_path, output_path, max_size_kb)
            print(f"Compressed {filename} to {output_path}")


source_folder = 'C:\\Users\\vikra\\Desktop\\pic1'
destination_folder = 'C:\\Users\\vikra\\Desktop\\pic3'

compress_images_in_folder(source_folder, destination_folder, 900)
