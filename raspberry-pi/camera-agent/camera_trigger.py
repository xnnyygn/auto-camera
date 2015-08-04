import os
from time import sleep

import RPi.GPIO as GPIO

PIN_LED = 22 
PIN_PIR = 23 

last_status = GPIO.LOW

def loop():
  global last_status
  current_status = GPIO.input(PIN_PIR)
  if current_status == GPIO.HIGH:
    GPIO.output(PIN_LED, GPIO.HIGH)
    if last_status == GPIO.LOW:
      print 'taking photo'
  else:
    GPIO.output(PIN_LED, GPIO.LOW)
  last_status = current_status 
  sleep(0.1)

if __name__ == '__main__':
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(PIN_LED, GPIO.OUT)
  GPIO.setup(PIN_PIR, GPIO.IN)

  try:
    while True:
      loop()
  except KeyboardInterrupt:
    GPIO.cleanup()