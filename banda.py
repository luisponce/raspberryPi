import wiringpi2 as gpio
import time
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = "10.0.58.229"

s.connect((ip, 8083))

gpio.wiringPiSetup()

pinL = 0
pinR = 1

s1 = 2
s2 = 3
s3 = 4
s4 = 5

gpio.pinMode(pinL, 1)
gpio.pinMode(pinR, 1)

gpio.pinMode(s1, 0)
gpio.pinMode(s2, 0)
gpio.pinMode(s3, 0)
gpio.pinMode(s4, 0)

lastSeen = 0

moving = 0

posS = 0

def getSensor(pos):
    if pos == 1: 
        return gpio.digitalRead(s1)
    if pos == 2:
        return gpio.digitalRead(s2)
    if pos == 3:
        return gpio.digitalRead(s3)
    if pos == 4:
        return gpio.digitalRead(s4)

def irA(pos):
    global moving
    global lastSeen
    if pos == 1:
        gpio.digitalWrite(pinR, 1)
        while getSensor(1)==0:
            pass
        gpio.digitalWrite(pinR, 0)
    if pos == 2:
        if lastSeen == 1:
            gpio.digitalWrite(pinL, 1)
            while getSensor(2)==0: 
                pass
            gpio.digitalWrite(pinL, 0)
        if lastSeen == 3 or lastSeen == 4:
            gpio.digitalWrite(pinR, 1)
            while getSensor(2)==0: 
                pass
            gpio.digitalWrite(pinR, 0)
    if pos == 3:
        if lastSeen == 1 or lastSeen == 2:
            gpio.digitalWrite(pinL, 1)
            while getSensor(3)==0: 
                pass
            gpio.digitalWrite(pinL, 0)
        if lastSeen == 4:
            gpio.digitalWrite(pinR, 1)
            while getSensor(3)==0:
                pass
            gpio.digitalWrite(pinR, 0)
    if pos == 4:
        gpio.digitalWrite(pinL, 1)
        while getSensor(4) == 0:
            pass
        gpio.digitalWrite(pinL, 0)

    moving = 0
    print("done")

def checkPos():
    global lastSeen
    if getSensor(1)==1:
        lastSeen = 1
    if getSensor(2)==1:
        lastSeen = 2
    if getSensor(3):
        lastSeen = 3
    if getSensor(4):
        lastSeen = 4



try:
    while 1:
        checkPos()
        print("lastSeen "+str(lastSeen))
        s.send(str(lastSeen)+"\n")
        if moving == 0:
            newPos = s.recv(1)
            print("r "+str(newPos))
            if newPos != posS:
                posS = newPos
                moving = 1
                irA(int(posS))
except KeyboardInterrupt:
    print("closing....")
    s.close()
