#!/usr/bin/env python3
# calibration.py – runs on startup to calibrate mic array using reference pinger.
import serial
import numpy as np
import time

# Reference pinger at known coordinates (x=0, y=0, z=2.0 m above array centre)
ref_pos = np.array([0.0, 0.0, 2.0])

def calibrate(ser, duration=10):
    """Collect TDOA lags from the reference pinger, compute phase offsets."""
    offsets = np.zeros(16)
    # ... collect data, solve for fixed offsets per channel
    # Write offsets to FPGA via serial command
    ser.write(b'CAL ' + offsets.tobytes())
    return offsets