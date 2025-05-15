# WYP-Pi Project Overview

## Current Status

This project aims to control a 16x16 NeoPixel matrix (256 LEDs) using a Raspberry Pi Zero. Here's what has been accomplished so far:

### Environment Setup
- Confirmed Raspberry Pi Zero as the target hardware
- Created Python virtual environment for development
- Enabled SPI interface (`sudo raspi-config nonint do_spi 0`)
- Installed required libraries:
  - adafruit-circuitpython-neopixel
  - rpi_ws281x

### Hardware Configuration
- 16x16 NeoPixel matrix connected to Raspberry Pi Zero
- Using a level shifter between Pi's 3.3V logic and NeoPixel's 5V requirement
- Default configuration uses GPIO 18 for data
- Power supplied externally (not through Pi)

### Code Development
Created several scripts to test and control the NeoPixel matrix:

1. `neopixel_test.py` - Basic test using Adafruit CircuitPython library
2. `check_neopixel_pin.py` - Tool to identify which GPIO pin is connected
3. `simple_neopixel.py` - Basic test using direct rpi_ws281x library
4. `pin_test.py` - Tool to test multiple GPIO pins
5. `matrix_display.py` - Advanced patterns for the matrix display
6. `check_sudo.py` - Tool to verify sudo permissions

### Current Issues
- LED matrix not lighting up when running test scripts
- Possible pin configuration issues (trying pin 18 vs pin 12 for GPIO 18)
- May need to address permission issues between sudo and venv

### Next Steps
1. Debug why LEDs aren't lighting up:
   - Test different GPIO pins systematically
   - Check physical connections
   - Check power supply
   - Verify level shifter is working correctly

2. Once basic functionality works:
   - Implement more advanced patterns
   - Create a web interface or control application
   - Set up scripts to run on boot

## Documentation
- README.md contains full instructions for setup and use
- All scripts are documented with comments
- Scripts accept command-line parameters for configuration

## Known Challenges
- NeoPixel libraries require sudo access for GPIO control
- Managing dependencies between system Python and virtual environment
- Ensuring proper power for all 256 LEDs (can draw significant current when all lit)