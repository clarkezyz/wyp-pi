#!/usr/bin/env python3
import os
import sys

def check_sudo():
    """Check if the script is running with sudo privileges"""
    return os.geteuid() == 0

print(f"Running as sudo: {check_sudo()}")
print(f"Executable path: {sys.argv[0]}")
print(f"User ID: {os.geteuid()}")
print(f"Group ID: {os.getegid()}")

print("\nIf running as sudo returns False, you need to run with sudo:")
print("sudo python3 check_sudo.py")

# Check for /dev/mem access
try:
    with open('/dev/mem', 'rb') as f:
        print("Successfully opened /dev/mem (required for NeoPixel library)")
except PermissionError:
    print("Permission denied when accessing /dev/mem. You need to run with sudo.")
except Exception as e:
    print(f"Error accessing /dev/mem: {str(e)}")