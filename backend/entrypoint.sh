#!/bin/bash

# Check if /dev/ttyUSB0 exists
if [ -e /dev/ttyUSB0 ]; then
  echo "Serial device /dev/ttyUSB0 found. Starting with serial device..."
else
  echo "No serial device found. Starting without serial device..."
fi

# Run the Flask app (or any other command you need)
exec python main.py
