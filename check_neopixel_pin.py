#!/usr/bin/env python3
import sys
import time
import board
import neopixel

def test_pin(pin_name, num_pixels=256):
    """Test a specific pin with a simple color sequence"""
    print(f"Testing pin {pin_name}...")
    
    try:
        pin = getattr(board, pin_name)
        pixels = neopixel.NeoPixel(
            pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=neopixel.GRB
        )
        
        # Red
        print(f"  Setting to red on {pin_name}")
        pixels.fill((255, 0, 0))
        pixels.show()
        time.sleep(1)
        
        # Green
        print(f"  Setting to green on {pin_name}")
        pixels.fill((0, 255, 0))
        pixels.show()
        time.sleep(1)
        
        # Blue
        print(f"  Setting to blue on {pin_name}")
        pixels.fill((0, 0, 255))
        pixels.show()
        time.sleep(1)
        
        # Off
        print(f"  Turning off on {pin_name}")
        pixels.fill((0, 0, 0))
        pixels.show()
        
        print(f"Test on {pin_name} completed.\n")
        return True
        
    except Exception as e:
        print(f"Error on pin {pin_name}: {str(e)}\n")
        return False

if __name__ == "__main__":
    # Common pins used for NeoPixels on Raspberry Pi
    default_pins = ['D18', 'D10', 'D12', 'D21']
    
    # Check if a specific pin is provided as an argument
    if len(sys.argv) > 1:
        pin_to_test = sys.argv[1]
        test_pin(pin_to_test)
    else:
        print("Testing common NeoPixel pins. Press Ctrl+C to stop at any time.")
        print("If the LEDs light up, remember the pin name that worked!")
        
        try:
            # Test each common pin
            for pin in default_pins:
                test_pin(pin)
                time.sleep(0.5)  # Small pause between pin tests
            
            print("All common pins tested. If none worked, try a specific pin.")
            print("Available pins:", [pin for pin in dir(board) if not pin.startswith('__') and pin.startswith('D')])
            print("\nUsage: python3 check_neopixel_pin.py PIN_NAME")
            print("Example: python3 check_neopixel_pin.py D5")
            
        except KeyboardInterrupt:
            print("\nTest interrupted by user.")