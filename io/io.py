import Adafruit_DHT
import time
import RPi.GPIO as GPIO

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
GPIO.setmode(GPIO.BOARD)
GPIOInputPins = [10,12,16,18]
for pin in GPIOInputPins:
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
def GetPinInputs():
    pressed = []
    for pin in GPIOInputPins:
        pressed.append(GPIO.input(pin)==GPIO.HIGH)
    return pressed;

while True:
    #humidity, temp = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    #if temp is not None:
        #print("Temp = {0:0.1f}C".format(temp))   
    #time.sleep(3);
    if any(pin for pin in GetPinInputs()):
        print("Yes")
    else:
        print("No")