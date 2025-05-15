#!/usr/bin/env python3
import time
import argparse
import board
import neopixel
import random

# Set up argument parser
parser = argparse.ArgumentParser(description='Display patterns on a 16x16 NeoPixel matrix.')
parser.add_argument('--pin', default='D18', help='GPIO pin (in board numbering) connected to NeoPixels')
parser.add_argument('--brightness', type=float, default=0.2, help='Brightness level (0.0 to 1.0)')
parser.add_argument('--pattern', default='rainbow', 
                    choices=['rainbow', 'bounce', 'sparkle', 'wipe', 'pulse', 'spiral'],
                    help='Pattern to display')
args = parser.parse_args()

# Matrix dimensions
WIDTH = 16
HEIGHT = 16
NUM_PIXELS = WIDTH * HEIGHT

# Create NeoPixel object
pixel_pin = getattr(board, args.pin)
pixels = neopixel.NeoPixel(
    pixel_pin, NUM_PIXELS, brightness=args.brightness, auto_write=False, pixel_order=neopixel.GRB
)

def xy_to_index(x, y):
    """Convert x,y coordinates to pixel index
    For serpentine layout (zigzag) common in 16x16 matrices"""
    if y % 2 == 0:
        # Even rows go left to right
        return y * WIDTH + x
    else:
        # Odd rows go right to left
        return y * WIDTH + (WIDTH - 1 - x)

def index_to_xy(index):
    """Convert pixel index to x,y coordinates"""
    y = index // WIDTH
    if y % 2 == 0:
        # Even rows go left to right
        x = index % WIDTH
    else:
        # Odd rows go right to left
        x = WIDTH - 1 - (index % WIDTH)
    return x, y

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

def clear():
    """Clear the display"""
    pixels.fill((0, 0, 0))
    pixels.show()

def rainbow_cycle(wait=0.01, cycles=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(255 * cycles):
        for i in range(NUM_PIXELS):
            pixel_index = (i * 256 // NUM_PIXELS) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

def color_wipe(color, wait=0.01):
    """Wipe color across display a pixel at a time."""
    for i in range(NUM_PIXELS):
        pixels[i] = color
        pixels.show()
        time.sleep(wait)

def bounce(color=(255, 0, 0), iterations=100, size=3, wait=0.05):
    """Bounce a dot across the matrix."""
    x, y = 0, 0
    dx, dy = 1, 1

    for _ in range(iterations):
        # Clear all pixels
        pixels.fill((0, 0, 0))
        
        # Draw the dot and its trail
        for i in range(size):
            trail_x = x - i * dx if 0 <= x - i * dx < WIDTH else x
            trail_y = y - i * dy if 0 <= y - i * dy < HEIGHT else y
            
            # Calculate color intensity for trail
            intensity = 1.0 - (i / size)
            trail_color = tuple(int(c * intensity) for c in color)
            
            # Set the pixel
            if 0 <= trail_x < WIDTH and 0 <= trail_y < HEIGHT:
                pixels[xy_to_index(trail_x, trail_y)] = trail_color
        
        pixels.show()
        time.sleep(wait)
        
        # Update position
        x += dx
        y += dy
        
        # Bounce off edges
        if x >= WIDTH - 1 or x <= 0:
            dx = -dx
        if y >= HEIGHT - 1 or y <= 0:
            dy = -dy

def sparkle(iterations=50, density=10, wait=0.05):
    """Random sparkle effect."""
    for _ in range(iterations):
        pixels.fill((0, 0, 0))
        
        # Light up random pixels
        for _ in range(density):
            i = random.randint(0, NUM_PIXELS - 1)
            pixels[i] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        pixels.show()
        time.sleep(wait)

def pulse(color=(0, 0, 255), iterations=5):
    """Pulse the entire display."""
    for _ in range(iterations):
        # Fade in
        for i in range(100):
            brightness = i / 100.0
            pixels.fill([int(c * brightness) for c in color])
            pixels.show()
            time.sleep(0.01)
        
        # Fade out
        for i in range(100, 0, -1):
            brightness = i / 100.0
            pixels.fill([int(c * brightness) for c in color])
            pixels.show()
            time.sleep(0.01)

def spiral(wait=0.05, iterations=2):
    """Create a spiral pattern across the matrix."""
    for _ in range(iterations):
        # Define spiral path
        x, y = WIDTH // 2, HEIGHT // 2
        dx, dy = 0, -1
        steps = 1
        step_count = 0
        spiral_path = []
        
        for i in range(NUM_PIXELS):
            spiral_path.append((x, y))
            
            # Move to next position
            if step_count == steps:
                step_count = 0
                # Change direction: right -> down -> left -> up
                dx, dy = -dy, dx
                if dy == 0:  # Completed a full turn
                    steps += 1
            
            x += dx
            y += dy
            step_count += 1
            
            # Check if we're outside the matrix
            if not (0 <= x < WIDTH and 0 <= y < HEIGHT):
                break
        
        # Light up the spiral
        for x, y in spiral_path:
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                idx = xy_to_index(x, y)
                hue = (idx * 2) % 256
                pixels[idx] = wheel(hue)
                pixels.show()
                time.sleep(wait)
        
        # Hold the final spiral briefly
        time.sleep(1)
        
        # Turn off in reverse order
        for x, y in reversed(spiral_path):
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                pixels[xy_to_index(x, y)] = (0, 0, 0)
                pixels.show()
                time.sleep(wait / 2)

try:
    print(f"Running {args.pattern} pattern on a 16x16 NeoPixel matrix")
    print(f"Connected to pin {args.pin} with brightness {args.brightness}")
    print("Press Ctrl+C to exit")
    
    # Clear display
    clear()
    
    # Run the selected pattern
    if args.pattern == 'rainbow':
        while True:
            rainbow_cycle()
    elif args.pattern == 'bounce':
        while True:
            bounce(color=(255, 0, 0), wait=0.03)  # Red
            bounce(color=(0, 255, 0), wait=0.03)  # Green
            bounce(color=(0, 0, 255), wait=0.03)  # Blue
    elif args.pattern == 'sparkle':
        while True:
            sparkle()
    elif args.pattern == 'wipe':
        while True:
            color_wipe((255, 0, 0))  # Red
            color_wipe((0, 255, 0))  # Green
            color_wipe((0, 0, 255))  # Blue
            color_wipe((0, 0, 0))    # Off
    elif args.pattern == 'pulse':
        while True:
            pulse((255, 0, 0))    # Red
            pulse((0, 255, 0))    # Green
            pulse((0, 0, 255))    # Blue
            pulse((255, 255, 0))  # Yellow
    elif args.pattern == 'spiral':
        while True:
            spiral()

except KeyboardInterrupt:
    # Turn off all pixels on exit
    clear()
    print("Program ended by user")