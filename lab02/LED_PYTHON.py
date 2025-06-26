#!/usr/bin/python3
import time
def export_gpio(pin):
   with open('/sys/class/gpio/export', 'w') as f:
       f.write(str(pin))
def unexport_gpio(pin):
   with open('/sys/class/gpio/unexport', 'w') as f:
       f.write(str(pin))
def set_direction(pin, direction):
   with open(f'/sys/class/gpio/gpio{pin}/direction', 'w') as f:
       f.write(direction)
def write_value(pin, value):
   with open(f'/sys/class/gpio/gpio{pin}/value', 'w') as f:
       f.write(str(value))
def acender_led(pin, duration):
   export_gpio(pin)
   set_direction(pin, 'out')
   write_value(pin, 1)
   time.sleep(duration)
   write_value(pin, 0)
   unexport_gpio(pin)


# Sequência de LEDs - Repetir 5 vezes
for i in range(5):
   # LED vermelho - GPIO 20
   acender_led(20, 2)
   # LED verde - GPIO 21
   acender_led(21, 1)
   # LED amarelo - GPIO 16
   acender_led(16, 1)
