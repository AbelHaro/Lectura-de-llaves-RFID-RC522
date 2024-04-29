import time
import wifi_connect as wifi
import data_sending_api as sender
import sensor
import led_control as led
import ubidots

wifi.connect()

uid = '01'
    
print(sender.add_user_register(uid))
print(sender.add_time_registry(uid))

# try:
#     while True:
#         #sender.add_time_registry(uid)
#         #sender.add_user_register(uid)
#         #sender.get_user_registered_by_uid(uid)
#         led.blink_led(sensor.read_sensor())
#         time.sleep(1)
# except KeyboardInterrupt:
#     print('Programa abortado con CTRL+C desde main.py')

# try:
#     while True:
#         led.blink_led(sensor.read_sensor()['api_status'])
#         time.sleep(1)
# except KeyboardInterrupt:
#     print('Programa abortado con CTRL+C desde main.py')
    



