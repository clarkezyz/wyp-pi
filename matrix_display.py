#!/usr/bin/env python3
import time
import sys
import argparse
from rpi_ws281x import PixelStrip, Color

# Matrix configuration
class NeoMatrix:
    def __init__(self, width=16, height=16, pin=18, brightness=50, channel=0):
        self.WIDTH = width
        self.HEIGHT = height
        self.NUM_PIXELS = width * height
        
        # LED strip configuration
        self.LED_PIN = pin
        self.LED_FREQ_HZ = 800000
        self.LED_DMA = 10
        self.LED_BRIGHTNESS = brightness
        self.LED_INVERT = False
        self.LED_CHANNEL = channel
        
        # Create and initialize the NeoPixel strip
        self.strip = PixelStrip(
            self.NUM_PIXELS, 
            self.LED_PIN, 
            self.LED_FREQ_HZ, 
            self.LED_DMA, 
            self.LED_INVERT, 
            self.LED_BRIGHTNESS,
            self.LED_CHANNEL
        )
        self.strip.begin()
        
    def xy_to_index(self, x, y):
        """Convert x,y coordinates to LED index, zigzag pattern"""
        if y % 2 == 0:
            # Even rows go left to right
            return y * self.WIDTH + x
        else:
            # Odd rows go right to left
            return y * self.WIDTH + (self.WIDTH - 1 - x)
    
    def fill(self, color):
        """Fill the entire matrix with one color"""
        for i in range(self.NUM_PIXELS):
            self.strip.setPixelColor(i, color)
        self.strip.show()
    
    def clear(self):
        """Clear the matrix (turn off all pixels)"""
        self.fill(Color(0, 0, 0))

    def set_pixel(self, x, y, color):
        """Set a single pixel by x,y coordinates"""
        if 0 <= x < self.WIDTH and 0 <= y < self.HEIGHT:
            self.strip.setPixelColor(self.xy_to_index(x, y), color)
    
    def show(self):
        """Update the display with current pixel values"""
        self.strip.show()

    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

# Display patterns
def color_wipe(matrix, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(matrix.NUM_PIXELS):
        matrix.strip.setPixelColor(i, color)
        matrix.strip.show()
        time.sleep(wait_ms/1000.0)

def rainbow_cycle(matrix, wait_ms=20, iterations=1):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(matrix.NUM_PIXELS):
            matrix.strip.setPixelColor(i, matrix.wheel((i + j) & 255))
        matrix.strip.show()
        time.sleep(wait_ms/1000.0)

def crosshair(matrix, color, wait_ms=200, iterations=10):
    """Moving crosshair pattern."""
    for _ in range(iterations):
        for x in range(matrix.WIDTH):
            # Clear previous pixels
            matrix.clear()
            
            # Draw horizontal line
            for i in range(matrix.WIDTH):
                matrix.set_pixel(i, x, color)
                
            # Draw vertical line
            for i in range(matrix.HEIGHT):
                matrix.set_pixel(x, i, color)
                
            matrix.show()
            time.sleep(wait_ms/1000.0)

def spiral(matrix, wait_ms=50):
    """Draw a spiral pattern inward and outward."""
    # Create a spiral path
    path = []
    x, y = matrix.WIDTH // 2, matrix.HEIGHT // 2
    dx, dy = 1, 0
    
    steps = 1
    step_count = 0
    max_steps = max(matrix.WIDTH, matrix.HEIGHT) * 2
    
    for _ in range(matrix.NUM_PIXELS):
        if 0 <= x < matrix.WIDTH and 0 <= y < matrix.HEIGHT:
            path.append((x, y))
        
        # Move to next position
        x, y = x + dx, y + dy
        step_count += 1
        
        if step_count == steps:
            step_count = 0
            dx, dy = -dy, dx
            if dy == 0:  # Completed a full turn
                steps += 1
                
        if steps > max_steps:
            break
    
    # Spiral inward - light up pixels along the path
    matrix.clear()
    for i, (x, y) in enumerate(path):
        color = matrix.wheel((i * 4) % 255)
        matrix.set_pixel(x, y, color)
        matrix.show()
        time.sleep(wait_ms / 1000.0)
    
    time.sleep(0.5)
    
    # Spiral outward - turn off pixels along the path
    for x, y in reversed(path):
        matrix.set_pixel(x, y, Color(0, 0, 0))
        matrix.show()
        time.sleep(wait_ms / 2000.0)

def bounce(matrix, color, iterations=10, wait_ms=50):
    """Bounce a pixel/ball around the matrix."""
    x, y = 0, 0
    dx, dy = 1, 1
    
    for _ in range(iterations):
        # Clear previous position
        matrix.clear()
        
        # Draw pixel at current position
        matrix.set_pixel(x, y, color)
        matrix.show()
        
        # Update position
        x += dx
        y += dy
        
        # Bounce off edges
        if x >= matrix.WIDTH - 1 or x <= 0:
            dx = -dx
        if y >= matrix.HEIGHT - 1 or y <= 0:
            dy = -dy
            
        time.sleep(wait_ms / 1000.0)

def display_text(matrix, text, color=Color(255, 255, 255), speed=0.1):
    """Display scrolling text using a simplified font."""
    # Simple 5x7 font (very basic implementation)
    # This will be highly simplified for demonstration purposes
    # In practice, you'd want a more complete font system
    
    # Clear the matrix
    matrix.clear()
    
    # Display the text "Hi!" as an example
    # H pattern
    x_offset = 0
    
    for x_offset in range(matrix.WIDTH, -20, -1):
        matrix.clear()
        
        # Draw a simple 'HI!' using simple patterns
        # H letter
        for i in range(7):
            matrix.set_pixel(x_offset, i, color)  # Left vertical
            matrix.set_pixel(x_offset + 4, i, color)  # Right vertical
            
        for i in range(5):
            if i == 2:  # Middle horizontal
                matrix.set_pixel(x_offset + i, 3, color)
        
        # I letter
        for i in range(7):
            matrix.set_pixel(x_offset + 6, i, color)  # Middle vertical
            
        # ! mark
        for i in range(5):
            matrix.set_pixel(x_offset + 8, i, color)  # Top vertical
        matrix.set_pixel(x_offset + 8, 6, color)  # Bottom dot
        
        matrix.show()
        time.sleep(speed)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Control a 16x16 NeoPixel Matrix')
    parser.add_argument('--pin', type=int, default=18, help='GPIO pin number')
    parser.add_argument('--brightness', type=int, default=50, help='Brightness (0-255)')
    parser.add_argument('--pattern', type=str, default='all',
                      choices=['rainbow', 'wipe', 'crosshair', 'spiral', 'bounce', 'text', 'all'],
                      help='Pattern to display')
    args = parser.parse_args()
    
    # Initialize matrix
    matrix = NeoMatrix(pin=args.pin, brightness=args.brightness)
    
    try:
        print(f"NeoPixel Matrix Demo - Pin: {args.pin}, Brightness: {args.brightness}")
        print("Press Ctrl+C to exit")
        
        if args.pattern == 'rainbow' or args.pattern == 'all':
            print("Rainbow cycle pattern")
            rainbow_cycle(matrix)
            matrix.clear()
            
        if args.pattern == 'wipe' or args.pattern == 'all':
            print("Color wipe pattern")
            color_wipe(matrix, Color(255, 0, 0))  # Red
            color_wipe(matrix, Color(0, 255, 0))  # Green
            color_wipe(matrix, Color(0, 0, 255))  # Blue
            color_wipe(matrix, Color(0, 0, 0))    # Off
            
        if args.pattern == 'crosshair' or args.pattern == 'all':
            print("Crosshair pattern")
            crosshair(matrix, Color(255, 255, 0))
            matrix.clear()
            
        if args.pattern == 'spiral' or args.pattern == 'all':
            print("Spiral pattern")
            spiral(matrix)
            matrix.clear()
            
        if args.pattern == 'bounce' or args.pattern == 'all':
            print("Bounce pattern")
            bounce(matrix, Color(0, 0, 255), iterations=30)
            matrix.clear()
            
        if args.pattern == 'text' or args.pattern == 'all':
            print("Text scrolling")
            display_text(matrix, "HI!")
            matrix.clear()
            
        # If a specific pattern was chosen, run it continuously
        if args.pattern != 'all':
            print(f"Running {args.pattern} pattern continuously. Press Ctrl+C to exit.")
            while True:
                if args.pattern == 'rainbow':
                    rainbow_cycle(matrix)
                elif args.pattern == 'wipe':
                    color_wipe(matrix, Color(255, 0, 0))
                    color_wipe(matrix, Color(0, 255, 0))
                    color_wipe(matrix, Color(0, 0, 255))
                    color_wipe(matrix, Color(0, 0, 0))
                elif args.pattern == 'crosshair':
                    crosshair(matrix, Color(255, 255, 0))
                elif args.pattern == 'spiral':
                    spiral(matrix)
                elif args.pattern == 'bounce':
                    bounce(matrix, Color(0, 0, 255), iterations=30)
                elif args.pattern == 'text':
                    display_text(matrix, "HI!")
        
    except KeyboardInterrupt:
        print("Exiting...")
        matrix.clear()

if __name__ == "__main__":
    if not sys.argv[0].startswith('sudo'):
        print("This script must be run with sudo privileges.")
        print("Usage: sudo python3 matrix_display.py [--pin PIN] [--brightness BRIGHTNESS] [--pattern PATTERN]")
        sys.exit(1)
        
    main()