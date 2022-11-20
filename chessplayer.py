from microbit import *
import radio

radio.on()

my_channel = 10
radio.config(channel=my_channel)

state = 'idle'

while True:
    if state == 'idle':
        if accelerometer.was_gesture("3g"):
            radio.send('online!')
            state = 'online!'
    if state == 'online!':
        message = radio.receive()
        if message:
            display.scroll(message)
            sleep(100)
            radio.send('message received!')
            state = 'idle'