import os
import subprocess
import argparse

def generate_thumbnail(video_path, thumbnail_path):
    """Generates a thumbnail for the given MP4 file and overwrites if it exists."""
    subprocess.run(
        [
            "ffmpeg", "-i", video_path, "-ss", "00:00:01", "-vframes", "1",
            "-vf", "scale=150:113:force_original_aspect_ratio=decrease",  # Resize to match first script
            "-y",  # Overwrite existing file
            thumbnail_path
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def process_folders(root_folder):
    """Processes each folder inside the root folder, generating thumbnails for MP4 files."""
    for foldername, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith(".mp4"):
                video_path = os.path.join(foldername, filename)
                thumbnail_path = os.path.join(foldername, filename.rsplit(".", 1)[0] + "_tn.jpg")
                generate_thumbnail(video_path, thumbnail_path)

def main():
    parser = argparse.ArgumentParser(description="Generate thumbnails for MP4 files in a directory.")
    parser.add_argument("root_folder", help="Path to the root folder containing MP4 files.")
    args = parser.parse_args()

    process_folders(args.root_folder)
    print("Thumbnail generation complete.")

if __name__ == "__main__":
    main()
