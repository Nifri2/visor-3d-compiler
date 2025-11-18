from pprint import pprint
import numpy as np
import argparse
import json
from rich.console import Console

console = Console()


def transform(
        frame, # numpy array of shape (H, W, 3) representing an image
        rotation=0, # degrees (0, 90, 180, 270)
        matrix_size=(16, 16), # (width, height) of the LED matrix
        brightness=1.0 # brightness factor (0.0 to 1.0)
    ):

    # Thank you so much numPy for making this so easy

    if rotation == 90:
        frame = np.rot90(frame, k=1)
    elif rotation == 180:
        frame = np.rot90(frame, k=2)
    elif rotation == 270:
        frame = np.rot90(frame, k=3)

    # The matrix does not follow a standard layout
    # It is a serpentine layout starting from bottom-right corner going left and upwards then right on the next row and so on.
    # we need to map the (x, y) coordinates to the correct index in the 1D array.

    height, width, _ = frame.shape
    transformed_frame = np.zeros((matrix_size[1], matrix_size[0], 3), dtype=np.uint8)

    for y in range(matrix_size[1]):
        for x in range(matrix_size[0]):
            if y % 2 == 0:
                mapped_x = matrix_size[0] - 1 - x
            else:
                mapped_x = x
            mapped_y = matrix_size[1] - 1 - y
            if mapped_x < width and mapped_y < height:
                transformed_frame[y, x] = frame[mapped_y, mapped_x][:3]
    # Apply brightness
    transformed_frame = np.clip(transformed_frame * brightness, 0, 255).astype(np.uint8)
    return transformed_frame

# transform a single frame of animation data by applying rotation, mapping it to the LED matrix layout, and adjusting brightness.

def transform_animation(animation_data, **kwargs):
    transformed_frames = []
    for frame_data in animation_data['frames']:
        frame = np.array(frame_data, dtype=np.uint8)
        transformed_frame = transform(frame, **kwargs)
        transformed_frames.append(transformed_frame.tolist())
    return transformed_frames


def run_transformation(input_file, output_file, **kwargs):
    """all this does is parse args and call transform_animation with all parameters from argparse, so we can import and use it in process.py"""
    with open(input_file, "r") as f:
        animation_data = json.load(f)

    transformed_animation = transform_animation(animation_data, **kwargs)

    with open(output_file, "w") as f:
        json.dump({"frames": transformed_animation}, f)

    with open("lambda.anim", "w") as f:
        for frame in transformed_animation:
            f.write(json.dumps(frame) + '\n')

    console.log(f"Animation transformed and saved to {output_file} :3")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Transform animation frames")
    parser.add_argument("input_file", type=str, help="Input animation JSON file")
    parser.add_argument("output_file", type=str, help="Output transformed animation file")
    parser.add_argument("--rotation", type=int, choices=[0, 90, 180, 270], default=0, help="Rotation angle")
    parser.add_argument("--matrix_width", type=int, default=16, help="LED matrix width")
    parser.add_argument("--matrix_height", type=int, default=16, help="LED matrix height")
    parser.add_argument("--brightness", type=float, default=1.0, help="Brightness factor (0.0 to 1.0)")

    args = parser.parse_args()

    with open(args.input_file, "r") as f:
        animation_data = json.load(f)

    transformed_animation = transform_animation(
        animation_data,
        rotation=args.rotation,
        matrix_size=(args.matrix_width, args.matrix_height),
        brightness=args.brightness
    )
    with open(args.output_file, "w") as f:
        json.dump({"frames": transformed_animation}, f)

    with open(args.output_file.replace(".json", ".anim"), "w") as f:
        for frame in transformed_animation:
            f.write(json.dumps(frame) + '\n')

    console.log(f"Animation transformed and saved to {args.output_file} :3")