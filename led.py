from gpiozero import LED
from time import sleep

led = LED(21)

while True:
    led.on()
    sleep(1)
    print("helo")
    led.off()
    sleep(1)
