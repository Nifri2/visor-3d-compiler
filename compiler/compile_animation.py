from PIL import Image
import numpy as np

import argparse
import json
import os

from rich.console import Console

console = Console()


def detect_image_sequence(input_dir):
    """Detects and returns a sorted list of image file paths in the input directory.
        They are sorted by frames, its blender output naming convention."""
    valid_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".tiff")
    image_files = [
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.lower().endswith(valid_extensions)
    ]
    image_files.sort()
    console.log(f"Detected {len(image_files)} image files.")
    return image_files

def compile_animation(image_files, output_file):
    """Compiles a sequence of images into a JSON animation file."""
    frames = []
    for img_path in image_files:
        with Image.open(img_path) as img:
            img_array = np.array(img)
            frames.append(img_array.tolist())  # Convert to list for JSON serialization

    animation_data = {
        "frames": frames,
        "num_frames": len(frames),
        "width": frames[0][0].__len__() if frames else 0,
        "height": frames[0].__len__() if frames else 0,
    }

    with open(output_file, "w") as f:
        json.dump(animation_data, f)

    console.log(f"Animation compiled and saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compile a sequence of images into an animation"
    )
    parser.add_argument(
        "input_dir", type=str, help="Directory containing input image sequence."
    )
    parser.add_argument(
        "output_file", type=str, help="Output JSON file for the animation."
    )
    args = parser.parse_args()
    image_files = detect_image_sequence(args.input_dir)

    compile_animation(image_files, args.output_file)
