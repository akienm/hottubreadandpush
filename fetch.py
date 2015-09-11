#!/usr/bin/python

# simple terminal program for raspberry pi to communicate with arduino
# this will eventually allow me to pass commands to the solar hot tub
# controller via a web page hosted on the pi

import time
import serial
import sys
import platform
import os


def PollKeyboard():
    import msvcrt
    import select
    inputchar = ''
    if platform.system() == 'Windows':
        if msvcrt.kbhit():
            inputchar = "%s" % msvcrt.getch()
    else:
        # must be linux
        i, o, e = select.select([sys.stdin], [], [], 0.0001)
        for s in i:
            if s == sys.stdin:
                inputchar = sys.stdin.read()
    if inputchar == "Q":
        sys.exit(0)
    return inputchar


def WriteChar(c):
    sys.stdout.write('%s' % c)
    sys.stdout.flush()

if platform.system() == 'Windows':
    ser = serial.Serial('COM8', 9600, timeout=1)   # Open serial port in arduino
else:
    # must be linux
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)   # Open serial port in arduino
    time.sleep(1)   #  Must be given. don't know why though! Doesn't execute properly if not given

ser.flushInput()  #Flush the buffers
ser.flushOutput()
buffer_to_push = ''
buffer = ''

while True:
    c = ser.read()
    if c == '<':
        buffer = '<'
    buffer += c
    if c == ">":
        buffer_to_push = buffer
        buffer = ''
    WriteChar(c)
    inputchar = ''
    inputchar = PollKeyboard()
    k = inputchar
    if k != '':
        sys.stdout.write( '%s' % k )
        ser.write(k)

ser.close()
print "DONE"