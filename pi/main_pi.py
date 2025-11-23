# Raspberry Pi animation player for two 16x16 NeoPixel matrices
# Uses rpi-ws281x-python library: https://github.com/rpi-ws281x/rpi-ws281x-python

import json
import time
from rpi_ws281x import Adafruit_NeoPixel, Color

# === LED strip configuration ===
# Matrix A
LED_COUNT_A = 256          # Number of LED pixels (16x16)
LED_PIN_A = 18             # GPIO pin connected to matrix A (PWM0)
LED_CHANNEL_A = 0          # '0' for GPIO18
# Matrix B
LED_COUNT_B = 256
LED_PIN_B = 13             # GPIO pin connected to matrix B (PWM1)
LED_CHANNEL_B = 1          # '1' for GPIO13

# Shared settings
LED_FREQ_HZ = 800000       # LED signal frequency in hertz (usually 800kHz)
LED_DMA = 10               # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255       # Set to 0 for darkest and 255 for brightest
LED_INVERT = False         # True to invert the signal (when using NPN transistor level shift)

# === Initialize both strips ===
strip_a = Adafruit_NeoPixel(LED_COUNT_A, LED_PIN_A, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL_A)
strip_b = Adafruit_NeoPixel(LED_COUNT_B, LED_PIN_B, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL_B)

strip_a.begin()
strip_b.begin()

# === Load animation files ===
# You can later change which files you load for each display
animation_a = []
animation_b = []

with open('eye_blink.anim') as f:
    for line in f:
        animation_a.append(json.loads(line))

with open('lambda.anim') as f:
    for line in f:
        animation_b.append(json.loads(line))

# === Main loop ===
last_time = time.time()
frame_count = 0

# with 2 displays we obviously half the framerate :<

while True:
    try:
        for frame_a, frame_b in zip(animation_a, animation_b):
            # --- Matrix A ---
            for y, row in enumerate(frame_a):
                for x, pixel in enumerate(row):
                    idx = y * 16 + x
                    strip_a.setPixelColor(idx, Color(pixel[0], pixel[1], pixel[2]))

            # --- Matrix B ---
            for y, row in enumerate(frame_b):
                for x, pixel in enumerate(row):
                    idx = y * 16 + x
                    strip_b.setPixelColor(idx, Color(pixel[0], pixel[1], pixel[2]))

            # Show both
            strip_a.show()
            strip_b.show()

            # FPS counter
            frame_count += 1
            now = time.time()
            if now - last_time >= 1.0:
                print(f"FPS: {frame_count}", end='\r')
                frame_count = 0
                last_time = now

    except KeyboardInterrupt:
        for s in [strip_a, strip_b]:
            for i in range(s.numPixels()):
                s.setPixelColor(i, Color(0, 0, 0))
            s.show()
        break
