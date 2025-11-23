import argparse
import struct
import json
import os
from rich.console import Console

console = Console()

def frame_to_binary(frame, width, height):
    """Converts a frame (list of lists of pixels) to a binary representation."""
    if len(frame) != height or any(len(row) != width for row in frame):
        raise ValueError(f"Frame shape must be {width}x{height}")

    b = bytearray()
    for row in frame:
        for pixel in row:
            r, g, b_val = pixel
            b.extend([r, g, b_val])
    return bytes(b)


def pack_animation(input_file, output_file, width=16, height=16):
    """
    Packs an animation from a JSON lines file into a binary format.
    """
    try:
        original_filesize = os.path.getsize(input_file)
    except FileNotFoundError:
        console.log(f"[red]Error: Input file not found: {input_file}[/red]")
        return

    pixels_per_frame = width * height
    bytes_per_frame = pixels_per_frame * 3

    frames = []
    with open(input_file, 'r') as f_in:
        for line in f_in:
            line = line.strip()
            if not line:
                continue
            try:
                frame = json.loads(line)
                frames.append(frame)
            except json.JSONDecodeError:
                console.log(f"[yellow]Warning: Skipping invalid JSON line in {input_file}[/yellow]")

    with open(output_file, 'wb') as f_out:
        # Write frame count
        f_out.write(struct.pack("<I", len(frames)))

        # Write frames
        for frame in frames:
            try:
                binary_frame = frame_to_binary(frame, width, height)
                f_out.write(binary_frame)
            except ValueError as e:
                console.log(f"[red]Error processing frame: {e}[/red]")
                # Decide whether to stop or continue
                return


    packed_size = len(frames) * bytes_per_frame + 4
    size_diff = original_filesize - packed_size
    console.log(f"Packed {len(frames)} frames into {output_file} ({packed_size} bytes; original size was {original_filesize} bytes; saved {size_diff} bytes, {size_diff / original_filesize * 100:.2f}% reduction).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pack 16x16 pixel animation into binary format.")
    parser.add_argument("input", help="Input animation file (JSON lines format)")
    parser.add_argument("output", help="Output binary file")
    parser.add_argument("--width", type=int, default=16, help="Width of the frames")
    parser.add_argument("--height", type=int, default=16, help="Height of the frames")
    args = parser.parse_args()

    pack_animation(args.input, args.output, args.width, args.height)
