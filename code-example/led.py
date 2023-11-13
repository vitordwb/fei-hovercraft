import json
from machine import Pin
from time import sleep

led = Pin(2, Pin.OUT)
btn = Pin(0)

while True:
  if btn.value() == 0:
      led.value(not led.value())
      
  sleep(0.5)