# NeoPixel 16x16 Matrix Controller for Raspberry Pi Zero

Scripts for controlling a 16x16 NeoPixel matrix (256 LEDs) on a Raspberry Pi Zero.

## Hardware Setup

- Raspberry Pi Zero
- 16x16 NeoPixel Matrix (256 LEDs)
- Level shifter (for converting 3.3V logic to 5V for the NeoPixels)
- Power supply (NeoPixels require 5V and sufficient current)

## Connection

Typically:
- Connect the NeoPixel data input to a GPIO pin (default is GPIO 18)
- Connect GND on the NeoPixel to GND on the Pi
- Use external 5V power for the NeoPixels (they draw too much current for the Pi)
- Use a level shifter between the Pi's 3.3V GPIO and the NeoPixel's 5V data in

## Installation

Make sure SPI is enabled:

```
sudo raspi-config nonint do_spi 0
```

Set up the virtual environment and install dependencies:

```
python3 -m venv venv
source venv/bin/activate
pip install adafruit-circuitpython-neopixel rpi_ws281x
```

## Scripts

### 1. Testing Sudo Access

NeoPixel scripts need to run with sudo. Test if your user has the right permissions:

```
python3 check_sudo.py
sudo python3 check_sudo.py  # This should work
```

### 2. Finding the correct pin

If you're unsure which GPIO pin your NeoPixel is connected to:

```
sudo python3 pin_test.py
```

This will test common pins (18, 12, 21, 10). If none work, you can test a specific pin:

```
sudo python3 pin_test.py 13
```

### 3. Basic Test

Run the simple test to ensure your matrix is working:

```
sudo python3 simple_neopixel.py
```

### 4. Advanced Matrix Display

Display various patterns on your 16x16 matrix:

```
sudo python3 matrix_display.py --pattern rainbow
```

Available patterns:
- rainbow
- wipe
- crosshair
- spiral
- bounce
- text
- all (runs all patterns in sequence)

You can also specify brightness and the GPIO pin:

```
sudo python3 matrix_display.py --pattern spiral --brightness 100 --pin 12
```

## CircuitPython API (Requires sudo)

The CircuitPython approach uses different GPIO pin numbering:

```
sudo python3 neopixel_test.py  # Uses board.D18 (GPIO 18)
```

```
sudo python3 check_neopixel_pin.py  # Tests multiple pins
```

## Troubleshooting

1. If no LEDs light up:
   - Check your physical connections
   - Ensure SPI is enabled (`sudo raspi-config nonint get_spi` should return 0)
   - Make sure you're running scripts with `sudo`
   - Try different GPIO pins with `pin_test.py`
   - Verify power supply (NeoPixels need 5V and enough current)

2. If only some LEDs work:
   - Check for loose connections
   - Try lowering the brightness (power issues)
   - Verify you're using the correct number of LEDs (256 for 16x16 matrix)
   - Look for broken LEDs or solder joints

3. If colors are wrong:
   - Try changing the color order (RGB, GRB, etc.) in the scripts