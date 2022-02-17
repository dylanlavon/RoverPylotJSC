#!/usr/bin/env python

'''
ps3rover20.py Drive the Brookstone Rover 2.0 via the P3 Controller, displaying
the streaming video using OpenCV.

Copyright (C) 2014 Simon D. Levy

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
'''

# Declare Button Constants (for XBOX360 Controller)
A = 0
B = 1
X = 2
Y = 3
LEFT_STICK_VERT = 1
RIGHT_STICK_VERT = 3
DRIFT_ADJUST = .05
PRESSED = 1

# Avoid button bounce by enforcing lag between button events
MIN_BUTTON_LAG_SEC = 0.1


# Import necessary modules
from rover import Rover20
import time
import pygame
import sys
import signal
#import controller
from pygame.locals import *

                                   
# Supports CTRL-C to override threads
def _signal_handler(signal, frame):
    frame.f_locals['rover'].close()
    sys.exit(0)

# Try to start OpenCV for video
try:
    import cv2
except:
    cv2 = None

# Begin Rover subclass for 360 + OpenCV ####################################################################################################
class PS3Rover(Rover20):

    def __init__(self):

        # Set up basics
        self.wname = 'Rover 2.0: Hold ESC to quit'
        self.quit = False

        pygame.init()

        # Set up controller using PyGame
        try:
            pygame.init()
            pygame.joystick.init()
            self.controller = pygame.joystick.Joystick(0)
            self.controller.init()
            self.usingController = True
            print("Using Controller")

        # Use Keyboard
        except:
            self.usingController = False
            self.treadFloat = [float(0),float(0)]
            self.treadstep = .5 # float value for rate of change
            self.changer = {
                -1: self.stop,
                119: self.moveForward,   # move forward
                97: self.turnLeft,    # move left
                115: self.moveBackward,   # move back
                100: self.turnRight,   # move right
                113: self.toggleLights,   # toggle lights WIP
                101: self.toggleStealth,   # toggle night vision WIP
                103: self.moveCameraDown,   # move camera down
                116: self.moveCameraUp,   # move camera up
                27: self.shutDown,   # close program
            }
            print("Using Keyboard")


         # Defaults on startup: lights off, ordinary camera
        self.lightsAreOn = False
        self.stealthIsOn = False

        # Tracks button-press times for debouncing
        self.lastButtonTime = 0


        Rover20.__init__(self)

    # Automagically called by Rover class
    def processVideo(self, jpegbytes, timestamp_10msec):
        # Update controller events
        if self.usingController:
            pygame.event.pump()
            print("CONTROLLERRRR")
        else:
            keyb = cv2.waitKey(1)
            try:
                self.changer[keyb]()
            except:
                self.changer[-1]
            self.setTreads(self.treadFloat[0], self.treadFloat[1])


        # Display video image if possible
        try:
            if cv2:
                # Save image to file on disk and load as Open2 image
                fname = 'tmp.jpg'
                fd = open(fname, 'wb')
                fd.write(bytes(jpegbytes))
                fd.close()
                image = cv2.imread(fname,1)
                # Show image
                cv2.imwrite(fname,image)
                cv2.imshow(self.wname, image)
                if cv2.waitKey(1) & 0xff == 27:
                    self.quit = True

            else:
                pass
        except:
            pass

        
    # Converts Y coordinate of specified axis to +/-1 or 0
    def axis(self, index):
        
        value = -self.controller.get_axis(index)
        
        if value > MIN_AXIS_ABSVAL:
            return 1
        elif value < -MIN_AXIS_ABSVAL:
            return -1
        else:
            return 0

    def stop(self):
        if self.treadFloat[0] < -self.treadstep:
            self.treadFloat[0]+=2*self.treadstep
        elif self.treadFloat[0] == -self.treadstep:
            self.treadFloat[0] += self.treadstep
        elif self.treadFloat[0] > self.treadstep:
            self.treadFloat[0] -= 2 * self.treadstep
        elif self.treadFloat[0] == self.treadstep:
            self.treadFloat[0] -= self.treadstep

        if self.treadFloat[1] < -self.treadstep:
            self.treadFloat[1] += 2 * self.treadstep
        elif self.treadFloat[1] == -self.treadstep:
            self.treadFloat[1] += self.treadstep
        elif self.treadFloat[1] > self.treadstep:
            self.treadFloat[1] -= 2 * self.treadstep
        elif self.treadFloat[1] == self.treadstep:
            self.treadFloat[1] -= self.treadstep
        self.moveCameraVertical(0)

        # a

    # Turn treads to turn rover left
    def turnLeft(self):
        print("Calling turnLeft")
        if self.treadFloat[0] > -1.0+self.treadstep:
            self.treadFloat[0] -= 2 * self.treadstep
        elif self.treadFloat[0] == -1.0+self.treadstep:
            self.treadFloat[0] -= self.treadstep

        if self.treadFloat[1] < 1.0-self.treadstep:
            self.treadFloat[1] += 2 * self.treadstep
        elif self.treadFloat[1] == 1.0-self.treadstep:
            self.treadFloat[1] += self.treadstep
        self.moveCameraVertical(0)


    # Turn treads to move rover forward
    def moveForward(self):
        print("Calling moveForward")
        if self.treadFloat[0] < 1.0 - self.treadstep:
            self.treadFloat[0] += 2 * self.treadstep
        elif self.treadFloat[0] == 1.0 - self.treadstep:
            self.treadFloat[0] += self.treadstep

        if self.treadFloat[1] < 1.0 - self.treadstep:
            self.treadFloat[1] += 2 * self.treadstep
        elif self.treadFloat[1] == 1.0 - self.treadstep:
            self.treadFloat[1] += self.treadstep
        self.moveCameraVertical(0)


    # Turn treads to turn rover right
    def turnRight(self):
        print("Calling turnRight")
        if self.treadFloat[0] < 1.0 - self.treadstep:
            self.treadFloat[0] += 2 * self.treadstep
        elif self.treadFloat[0] == 1.0 - self.treadstep:
            self.treadFloat[0] += self.treadstep

        if self.treadFloat[1] > -1.0 + self.treadstep:
            self.treadFloat[1] -= 2 * self.treadstep
        elif self.treadFloat[1] == -1.0 + self.treadstep:
            self.treadFloat[1] -= self.treadstep
        self.moveCameraVertical(0)


    # Turn treads to move rover backwards
    def moveBackward(self):
        print("Calling moveBackward")
        if self.treadFloat[0] > -1.0 + self.treadstep:
            self.treadFloat[0] -= 2 * self.treadstep
        elif self.treadFloat[0] == -1.0 + self.treadstep:
            self.treadFloat[0] -= self.treadstep

        if self.treadFloat[1] > -1.0 + self.treadstep:
            self.treadFloat[1] -= 2 * self.treadstep
        elif self.treadFloat[1] == -1.0 + self.treadstep:
            self.treadFloat[1] -= self.treadstep
        self.moveCameraVertical(0)


    # Toggle stealth mode (infrared camera)
    def toggleStealth(self):
        print("Calling toggleStealth")
        if self.stealthIsOn == False:
            self.turnStealthOn()
            self.stealthIsOn = True
        elif self.stealthIsOn == True:
            self.turnStealthOff()
            self.stealthIsOn = False


    # Toggle green lights
    def toggleLights(self):
        print("Calling toggleLights")
        if self.lightsAreOn == False:
            self.turnLightsOn()
            self.lightsAreOn = True
        elif self.lightsAreOn == True:
            self.turnLightsOff()
            self.lightsAreOn = False


    # Move camera down
    def moveCameraDown(self):
        print("Calling moveCameraDown")
        self.moveCameraVertical(-1)


    # Move camera up
    def moveCameraUp(self):
        print("Calling moveCameraUp")
        self.moveCameraVertical(1)


    # Close the program and turn of lights / stealth mode if enabled
    def shutDown(self):
        print("Closing Program")
        rover.turnLightsOff()
        rover.lightsAreOn = False
        rover.turnStealthOff()
        rover.stealthIsOn = False
        sys.exit()
        


    def checkKey(self,flag,keyID,keypresses,onRoutine=None,offRoutine=None):
        if keypresses[keyID]:
            if (time.time() - self.lastButtonTime) > MIN_BUTTON_LAG_SEC:
                self.lastButtonTime = time.time()
                if flag:
                    if offRoutine:
                        offRoutine()
                    flag = False
                else:
                    if onRoutine:
                        onRoutine()
                    flag = True
        return flag


    # Handles button bounce by waiting a specified time between button presses   
    def checkButton(self, flag, buttonID, onRoutine=None, offRoutine=None):
        if self.controller.get_button(buttonID):
            if (time.time() - self.lastButtonTime) > MIN_BUTTON_LAG_SEC:
                self.lastButtonTime = time.time()
                if flag:
                    if offRoutine:
                        offRoutine()
                    flag = False
                else:
                    if onRoutine:
                        onRoutine()
                    flag = True
        return flag
        
# main -----------------------------------------------------------------------------------

if __name__ == '__main__':

    # Create a PS3 Rover object
    rover = PS3Rover()

    # Set up signal handler for CTRL-C

    signal.signal(signal.SIGINT, _signal_handler)

    while rover.quit == False:
        pass

    rover.close()



