#!/usr/bin/env python3
import sys
import time
from rpi_ws281x import PixelStrip, Color

# LED strip default configuration:
LED_COUNT = 256        # 16x16 = 256 LEDs
LED_FREQ_HZ = 800000   # LED signal frequency in Hz (800 KHz)
LED_DMA = 10           # DMA channel
LED_BRIGHTNESS = 50    # 0-255, lower if flickering occurs
LED_INVERT = False     # True to invert the signal

def test_pin(pin):
    """Test a specific GPIO pin with the NeoPixel matrix"""
    print(f"Testing GPIO pin {pin}...")
    
    # Determine channel based on pin
    channel = 0
    if pin in [13, 19, 41, 45, 53]:
        channel = 1
    else:
        channel = 0
    
    # Create strip
    strip = PixelStrip(LED_COUNT, pin, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, channel)
    strip.begin()
    
    # Test with solid colors
    print(f"  Testing red on GPIO {pin}")
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(255, 0, 0))
    strip.show()
    time.sleep(1)
    
    print(f"  Testing green on GPIO {pin}")
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 255, 0))
    strip.show()
    time.sleep(1)
    
    print(f"  Testing blue on GPIO {pin}")
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 255))
    strip.show()
    time.sleep(1)
    
    # Turn off
    print(f"  Turning off LEDs on GPIO {pin}")
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
    
    print(f"Test completed for GPIO {pin}\n")

def main():
    # Common GPIO pins that can be used for NeoPixels on a Raspberry Pi
    default_pins = [18, 12, 21, 10]
    
    if len(sys.argv) > 1:
        # Test specific pin from command line
        try:
            pin = int(sys.argv[1])
            test_pin(pin)
        except ValueError:
            print(f"Error: '{sys.argv[1]}' is not a valid GPIO pin number")
            print("Usage: sudo python3 pin_test.py [GPIO_PIN_NUMBER]")
            print("Example: sudo python3 pin_test.py 21")
    else:
        # Test default pins
        print("Testing common GPIO pins for NeoPixel compatibility...")
        print("Press Ctrl+C to stop the test if LEDs light up.")
        print("(This indicates you've found the correct pin)")
        
        try:
            for pin in default_pins:
                test_pin(pin)
            
            print("All common pins tested. If none worked, try a specific pin.")
            print("Usage: sudo python3 pin_test.py [GPIO_PIN_NUMBER]")
            print("Example: sudo python3 pin_test.py 13")
            
        except KeyboardInterrupt:
            print("\nTest interrupted by user")

if __name__ == "__main__":
    if not sys.argv[0].startswith('sudo'):
        print("This script must be run with sudo privileges.")
        print("Usage: sudo python3 pin_test.py [GPIO_PIN_NUMBER]")
        sys.exit(1)
    
    main()