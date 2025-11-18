import argparse
import json
import os
import tempfile
import sys
from rich.console import Console

console = Console()

# Add the current directory to the path to ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from compile_animation import detect_image_sequence, compile_animation
from transformer import transform_animation

def main():
    """
    A wrapper script that compiles and transforms an animation from a sequence of images.
    It combines the functionality of compile-animation.py and transformer.py.
    """
    parser = argparse.ArgumentParser(
        description="Compile and transform an animation from a sequence of images.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Input directory
    parser.add_argument(
        "input_dir",
        type=str,
        help="Directory containing the input image sequence."
    )

    # Output directory
    parser.add_argument(
        "--output-dir",
        type=str,
        default="animations/compiled",
        help="Directory to save the transformed animation (default: animations/compiled)."
    )

    # Arguments from transformer.py
    parser.add_argument(
        "--rotation",
        type=int,
        choices=[0, 90, 180, 270],
        default=0,
        help="Rotation angle in degrees for the animation frames."
    )
    parser.add_argument(
        "--matrix_width",
        type=int,
        default=16,
        help="Width of the LED matrix."
    )
    parser.add_argument(
        "--matrix_height",
        type=int,
        default=16,
        help="Height of the LED matrix."
    )
    parser.add_argument(
        "--brightness",
        type=float,
        default=1.0,
        help="Brightness factor for the animation (from 0.0 to 1.0)."
    )

    args = parser.parse_args()

    # --- Step 1: Compile the animation ---
    console.log(f"Detecting image sequence in '{args.input_dir}'...")
    image_files = detect_image_sequence(args.input_dir)
    if not image_files:
        console.log("No image files found. Exiting.")
        return

    # Use a temporary file for the intermediate compiled animation
    temp_filename = ""
    try:
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".json") as temp_f:
            temp_filename = temp_f.name
        
        console.log(f"Compiling animation to temporary file: {temp_filename}")
        compile_animation(image_files, temp_filename)

        with open(temp_filename, "r") as f:
            animation_data = json.load(f)
    finally:
        # Clean up the temporary file
        if temp_filename and os.path.exists(temp_filename):
            os.unlink(temp_filename)

    # --- Step 2: Transform the animation ---
    console.log("Transforming animation...")
    transformed_frames = transform_animation(
        animation_data,
        rotation=args.rotation,
        matrix_size=(args.matrix_width, args.matrix_height),
        brightness=args.brightness
    )

    # --- Step 3: Save the final output ---
    input_dir_name = os.path.basename(os.path.normpath(args.input_dir))
    
    # Main output file (.animbyte)
    output_filename_base = os.path.splitext(input_dir_name)[0]
    output_filename = f"{output_filename_base}.animbyte"
    output_filepath = os.path.join(args.output_dir, output_filename)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
        console.log(f"Created output directory: {args.output_dir}")

    # with open(output_filepath, "w") as f:
    #     json.dump({"frames": transformed_frames}, f)
    # console.log(f"Transformed animation saved to {output_filepath}")

    with open(output_filepath.replace(".animbyte", ".anim"), "w") as f:
        for frame in transformed_frames:
            f.write(json.dumps(frame) + '\n')
    console.log(f"Transformed animation saved to {output_filepath.replace('.animbyte', '.anim')}")


    console.log("Done! :3")


if __name__ == "__main__":
    main()
