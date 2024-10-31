#this resizes images in cwd
import os
from PIL import Image

# Target size for resizing
target_size = (500, 500)

# Get the current directory
current_dir = os.getcwd()

# Loop through all files in the current directory
for filename in os.listdir(current_dir):
    # Check if the file is an image (modify extensions as needed)
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
        # Define the path for the image
        img_path = os.path.join(current_dir, filename)
        
        # Open, resize, and save the image
        with Image.open(img_path) as img:
            resized_img = img.resize(target_size)
            # Save the resized image with the same filename
                # Remove the original image
            os.remove(img_path)
            resized_img.save(img_path)
        
    

print("All images resized to 500x500 and originals removed.")
