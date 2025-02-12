import os
import sys
from PIL import Image

def create_thumbnails(root_folder, size=(150, 150)):
    """Generate thumbnails for all JPG images in subfolders."""
    for foldername, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith(".jpg"):
                image_path = os.path.join(foldername, filename)
                thumbnail_path = os.path.join(foldername, f"{os.path.splitext(filename)[0]}_tn.jpg")

                # Skip if thumbnail already exists
                if os.path.exists(thumbnail_path):
                    continue

                try:
                    with Image.open(image_path) as img:
                        img.thumbnail(size)
                        img.save(thumbnail_path, "JPEG")
                        print(f"Created thumbnail: {thumbnail_path}")
                except Exception as e:
                    print(f"Failed to create thumbnail for {image_path}: {e}")

# Run the function if the script is executed directly
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 create-tn.py <folder-path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    create_thumbnails(folder_path)
