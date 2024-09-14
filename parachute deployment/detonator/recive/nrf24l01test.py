from machine import Pin, SPI
import struct
from nrf24l01 import NRF24L01
import utime

led = Pin(25, Pin.OUT)                # LED
csn = Pin(17, mode=Pin.OUT, value=1)  # chip select not
ce  = Pin(5, mode=Pin.OUT, value=0)   # chip enable
mosfet = Pin(15, Pin.OUT)             # MOSFET control

# Addresses are in little-endian format. They correspond to big-endian
# 0xf0f0f0f0e1, 0xf0f0f0f0d2 - swap these on the other Pico!
pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")

def setup():
    print("Initializing the nRF24L01 Module")
    spi = SPI(0, baudrate=2000000, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
    nrf = NRF24L01(spi, csn, ce, payload_size=4)
    
    nrf.open_tx_pipe(pipes[1])
    nrf.open_rx_pipe(1, pipes[0])
    nrf.start_listening()

    led.value(0)
    mosfet.value(0)  # Make sure the MOSFET is off initially
    return nrf

def slave(nrf):
    while True:
        if nrf.any():
            buf = nrf.recv()
            got = struct.unpack("i", buf)[0]
            print("rx", got)
            if got == 1:
                led.value(1)
                mosfet.value(1)  # Turn on MOSFET
                                
                # Keep the MOSFET on for 5 seconds
                utime.sleep(5)
                mosfet.value(0)  # Turn off MOSFET
                print("MOSFET turned off")
                led.value(0)
                break  # Stop listening for further messages
        else:
            led.value(0)  # Turn off LED when no message is received

        utime.sleep(0.01)  # Small delay to avoid flooding

def auto_ack(nrf):
    nrf.reg_write(0x01, 0b11111000)  # enable auto-ack on all pipes

nrf = setup()
auto_ack(nrf)
slave(nrf)
