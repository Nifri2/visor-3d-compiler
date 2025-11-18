# rp2040 animation player

import os
import json
import time
from machine import Pin
from neopixel import NeoPixel

# Configure the NeoPixel strip
pin = Pin(0, Pin.OUT)
np = NeoPixel(pin, 256)  # 16x16 matrix


# Main loop to play the animation
while True:
    with open('lambda.anim') as f:
        for line in f:
            frame = json.loads(line)
            # Iterate over each pixel in the frame and set its color
            for y, row in enumerate(frame):
                for x, pixel in enumerate(row):
                    index = y * 16 + x
                    np[index] = tuple(pixel)

            # Update the NeoPixel strip to display the new frame
            np.write()


            # Pause between frames to control the animation speed (e.g., ~30 FPS)
            # time.sleep(1 / 60)
            # Comment: this is so slow on rp2040 that we don't need a delay
            # Estimated FPS is 13-15 FPS without delay

