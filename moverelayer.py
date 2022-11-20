from microbit import *
import radio

radio.on()

my_channel = 10

radio.config(channel=my_channel)

while True:
    message = radio.receive()
    if message == 'online!':
        enginemove = input("Move suggested? ")
        sleep(100)
        radio.send(enginemove)
    if message == "message received!":
        pass
