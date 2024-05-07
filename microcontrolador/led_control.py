from machine import Pin  # MicroPython machine module for hardware control
import time  # Standard Python time module

def blink_led(is_correct, correct_pin=12, incorrect_pin=13):
    """
    Blinks an LED based on whether a response is correct or incorrect.

    Parameters:
        is_correct (bool): Indicates if the response is correct (True) or incorrect (False).
        correct_pin (int): GPIO pin number for the correct LED (default: 12).
        incorrect_pin (int): GPIO pin number for the incorrect LED (default: 13).
    """
    # Initialize GPIO pins for correct and incorrect LEDs
    correct_led = Pin(correct_pin, Pin.OUT)
    incorrect_led = Pin(incorrect_pin, Pin.OUT)

    # Determine which LED to blink based on the response correctness
    if is_correct:
        # Turn on correct LED for 2 seconds
        correct_led.value(1)
        time.sleep(2)
        correct_led.value(0)  # Turn off correct LED after delay
    else:
        # Turn on incorrect LED for 2 seconds
        incorrect_led.value(1)
        time.sleep(2)
        incorrect_led.value(0)  # Turn off incorrect LED after delay