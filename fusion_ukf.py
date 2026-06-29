#!/usr/bin/env python3
# fusion_ukf.py – UKF sensor fusion with environmental compensation
import numpy as np
from filterpy.kalman import UnscentedKalmanFilter, MerweScaledSigmaPoints
import smbus2
import bme280

# ---------- BME280 Sound Speed ----------
def get_sound_speed():
    # Assume BME280 on I2C bus 1
    bus = smbus2.SMBus(1)
    calibration_params = bme280.load_calibration_params(bus, 0x76)
    data = bme280.sample(bus, 0x76, calibration_params)
    T = data.temperature  # °C
    RH = data.humidity    # %
    # Speed of sound adjusted for temperature and humidity
    c = 331.3 * np.sqrt(1 + T/273.15)
    # Add humidity correction (approx)
    c *= 1 + 0.14 * (RH / 100.0) * (T/273.15)
    return c

# ---------- UKF Setup ----------
points = MerweScaledSigmaPoints(n=6, alpha=0.1, beta=2., kappa=-3)
ukf = UnscentedKalmanFilter(dim_x=6, dim_z=3, dt=0.1, fx=state_transition, hx=measurement_func, points=points)
ukf.x = np.array([5., 0., 10., 0., 0., 0.])
ukf.P *= 0.1
# ...

def measurement_func(x):
    # Convert state [x,y,z,vx,vy,vz] into expected TDOAs or Cartesian coords
    # (depending on which sensor is being fused)
    return x[:3]   # simplified for direct position measurement

def state_transition(x, dt):
    F = np.eye(6)
    F[0,3] = F[1,4] = F[2,5] = dt
    return F @ x

# In the fusion loop, after receiving a new measurement:
def fuse_measurement(z, sensor_type, c):
    global ukf
    if sensor_type == 'ultrasonic':
        # Update speed of sound in measurement model
        # Recompute measurement noise based on c
        ukf.R = np.eye(3) * (0.01 * (c/343.0)**2)  # scale noise with sound speed
    ukf.predict()
    ukf.update(z)
    return ukf.x[:3]