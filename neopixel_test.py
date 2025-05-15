#!/usr/bin/env python3
import time
import board
import neopixel

# Define the pin connected to the NeoPixel data line
# Typically for Raspberry Pi, this would be D18 (GPIO 18)
pixel_pin = board.D18

# Define the number of NeoPixels
# 16x16 matrix = 256 pixels
num_pixels = 256

# Define the order of the pixel colors - RGB or GRB
# For most NeoPixel products, the first parameter should be 'GRB'
ORDER = neopixel.GRB

# Create the NeoPixel object
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

def fill_matrix():
    print("Filling matrix with red")
    pixels.fill((255, 0, 0))  # Red
    pixels.show()
    time.sleep(1)
    
    print("Filling matrix with green")
    pixels.fill((0, 255, 0))  # Green
    pixels.show()
    time.sleep(1)
    
    print("Filling matrix with blue")
    pixels.fill((0, 0, 255))  # Blue
    pixels.show()
    time.sleep(1)
    
    print("Turning off all pixels")
    pixels.fill((0, 0, 0))  # Off
    pixels.show()
    time.sleep(1)

def draw_pattern():
    # Draw a simple pattern (a cross)
    pixels.fill((0, 0, 0))  # Clear all
    
    # For a 16x16 matrix:
    for i in range(16):
        # Draw a horizontal line in the middle
        pixels[i + 16*7] = (255, 255, 0)  # Yellow horizontal line
        # Draw a vertical line in the middle
        pixels[7 + 16*i] = (0, 255, 255)  # Cyan vertical line
    
    pixels.show()
    time.sleep(2)

print("Testing 16x16 NeoPixel Matrix...")

try:
    while True:
        print("Running LED test sequence")
        
        # Test basic colors
        fill_matrix()
        
        # Test pattern
        draw_pattern()
        
        # Test rainbow effect
        print("Rainbow cycle")
        rainbow_cycle(0.01)  # Rainbow cycle with 10ms delay per step
        
except KeyboardInterrupt:
    # Turn off all pixels on exit
    pixels.fill((0, 0, 0))
    pixels.show()
    print("Program ended by user")