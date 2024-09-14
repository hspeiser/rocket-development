from machine import Pin, I2C, PWM
from bmp085 import BMP180
import time

# Constants
ALTITUDE_DROP_THRESHOLD = 100  # feet

# I2C setup for the sensor
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=40000)

bmp = BMP180(i2c)
bmp.oversample = 2
bmp.sealevel = 1010.5

# Servo setup
servo_pin = Pin(2, Pin.OUT)
servo = PWM(servo_pin)
servo.freq(50)

# Function to rotate servo
def rotate_servo(angle):
    min_pulse = 1000
    max_pulse = 2000
    pulse_width = min_pulse + (angle / 180) * (max_pulse - min_pulse)
    duty = int(pulse_width / 20000 * 65535)
    servo.duty_u16(duty)

# Function to average altitude for the first second
def zero_sensor():
    altitudes = []
    start_time = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start_time) < 1000:
        altitudes.append(bmp.altitude)
        time.sleep_ms(10)  # delay of 10 milliseconds
    return sum(altitudes) / len(altitudes)

# Main logic
def main():
    baseline_altitude = zero_sensor()
    print(f"Baseline Altitude: {baseline_altitude:.2f} feet")
    highest_altitude = float('-inf')

    while True:
        tempC = bmp.temperature    # get the temperature in degree celsius
        pres_hPa = bmp.pressure    # get the pressure in hPa
        altitude = bmp.altitude    # get the altitude
        temp_f = (tempC * (9/5) + 32)  # convert the temperature value to Fahrenheit
        
        current_altitude = altitude - baseline_altitude  # adjust based on baseline

        if current_altitude > highest_altitude:
            highest_altitude = current_altitude
        
        print(f"Temperature: {tempC:.2f}°C / {temp_f:.2f}°F, Pressure: {pres_hPa:.2f} hPa, Current Altitude: {current_altitude:.2f} feet, Highest Altitude: {highest_altitude:.2f} feet")

        if current_altitude <= (highest_altitude - ALTITUDE_DROP_THRESHOLD):
            print("Dropping altitude detected. Rotating servo.")
            rotate_servo(50)
            break

        time.sleep(0.05)  # delay of 1 second

if __name__ == "__main__":
    main()
