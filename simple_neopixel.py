#!/usr/bin/env python3
import time
from rpi_ws281x import PixelStrip, Color

# LED strip configuration:
LED_COUNT = 256        # 16x16 = 256 LEDs
LED_PIN = 18           # GPIO pin (18 uses PWM channel 0)
LED_FREQ_HZ = 800000   # LED signal frequency in Hz (800 KHz)
LED_DMA = 10           # DMA channel
LED_BRIGHTNESS = 50    # 0-255, lower if flickering occurs
LED_INVERT = False     # True to invert the signal
LED_CHANNEL = 0        # PWM channel 0 or 1

# Create the strip object
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Initialize the library
strip.begin()

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

# Main function
def main():
    print('Press Ctrl-C to quit.')
    try:
        while True:
            print('Testing basic colors...')
            # Color wipe animations
            colorWipe(strip, Color(255, 0, 0))  # Red
            colorWipe(strip, Color(0, 255, 0))  # Green
            colorWipe(strip, Color(0, 0, 255))  # Blue
            
            # Rainbow cycle
            print('Rainbow cycle...')
            rainbow(strip)
            
    except KeyboardInterrupt:
        # Turn off all LEDs
        colorWipe(strip, Color(0, 0, 0), 10)

if __name__ == '__main__':
    main()