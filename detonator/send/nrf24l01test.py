from machine import Pin, SPI
import struct
from nrf24l01 import NRF24L01
import utime

led = Pin(25, Pin.OUT)                # LED
csn = Pin(17, mode=Pin.OUT, value=1)  # chip select not
ce  = Pin(5, mode=Pin.OUT, value=0)   # chip enable
button = Pin(15, Pin.IN, Pin.PULL_UP) # Button input with pull-up resistor

# Addresses are in little-endian format. They correspond to big-endian
# 0xf0f0f0f0e1, 0xf0f0f0f0d2 - swap these on the other Pico!
pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")

def setup():
    print("Initializing the nRF24L01 Module")
    spi = SPI(0, baudrate=2000000, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
    nrf = NRF24L01(spi, csn, ce, payload_size=4)
    
    nrf.open_tx_pipe(pipes[0])
    nrf.open_rx_pipe(1, pipes[1])
    nrf.start_listening()

    led.value(0)
    return nrf

def master(nrf):
    while True:
        if button.value() == 0:  # Button is pressed
            led.value(1)  # Turn on LED to indicate message sending
            print("tx 1")
            nrf.stop_listening()
            try:
                nrf.send(struct.pack("i", 1))
                print("Message sent")
                utime.sleep(0.01)
            except OSError:
                print('Message lost')
        else:
            led.value(0)  # Turn off LED when button is not pressed
            utime.sleep(0.1)  # Small delay to avoid flooding

def auto_ack(nrf):
    nrf.reg_write(0x01, 0b11111000)  # enable auto-ack on all pipes

nrf = setup()
auto_ack(nrf)
master(nrf)
