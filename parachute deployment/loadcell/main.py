from hx711 import HX711
from machine import Pin
import utime
import os

class Scales(HX711):
    def __init__(self, d_out, pd_sck):
        super(Scales, self).__init__(d_out, pd_sck)
        self.offset = 0

    def reset(self):
        self.power_off()
        self.power_on()

    def tare(self):
        self.offset = self.read()

    def raw_value(self):
        return self.read() - self.offset

    def stable_value(self, reads=1, delay_us=500):
        return self.raw_value()

    @staticmethod
    def _stabilizer(values, deviation=10):
        weights = []
        for prev in values:
            weights.append(sum([1 for current in values if abs(prev - current) / (prev / 100) <= deviation]))
        return sorted(zip(values, weights), key=lambda x: x[1]).pop()[0]

def get_next_filename(prefix="loadcell_test_no_"):
    max_number = 0
    for file in os.listdir():
        if file.startswith(prefix):
            try:
                number = int(file[len(prefix):])
                if number > max_number:
                    max_number = number
            except ValueError:
                pass
    return f"{prefix}{max_number + 1}"

if __name__ == "__main__":
    filename = get_next_filename()
    
    # Initialize LED
    led = Pin("LED", Pin.OUT)  # Assuming LED is connected to GPIO 2, adjust as needed
    
    # Open the CSV file for writing
    with open(filename, 'w') as file:
        file.write("Milliseconds,Weight (grams)\n")
        
        scales = Scales(d_out=Pin(5), pd_sck=Pin(4))
        scales.tare()
        
        start_time = utime.ticks_ms()
        
        try:
            while True:
                led.on()  # Turn on LED
                val = scales.stable_value()
                weight = val * 0.00908376594
                elapsed_time = utime.ticks_diff(utime.ticks_ms(), start_time)
                print(weight)
                file.write("{},{}\n".format(elapsed_time, weight))
                file.flush()  # Ensure data is written to file immediately
                led.off()  # Turn off LED
                
        except KeyboardInterrupt:
            print("Scale measurement stopped by user.")
        
        scales.power_off()
        print("Scale measurement stopped.")
