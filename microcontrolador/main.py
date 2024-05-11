import time
import wifi_connect as wifi
import data_sending_api as sender
import sensor
import led_control as led
import ubidots

wifi.connect()

try:
    while True:
        response = sensor.read_sensor()
        led.blink_led(response['api_status'])
        time.sleep(1)
except KeyboardInterrupt:
    print('Programa abortado con CTRL+C desde main.py')
    



