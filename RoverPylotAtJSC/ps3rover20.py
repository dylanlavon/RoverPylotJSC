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

# You may want to adjust these buttons for your own controller
BUTTON_LIGHTS      = 2  # Square button toggles lights
BUTTON_STEALTH     = 1  # Circle button toggles stealth mode
BUTTON_CAMERA_UP   = 3  # Triangle button raises camera
BUTTON_CAMERA_DOWN = 0  # X button lowers camera

# Avoid button bounce by enforcing lag between button events
MIN_BUTTON_LAG_SEC = 0.1

# Avoid close-to-zero values on axis
MIN_AXIS_ABSVAL    = 0.01




from rover import Rover20

import time
import pygame
import sys
import signal
from pygame.locals import *

KEY_LIGHTS      = pygame.K_q  # Square button toggles lights
KEY_STEALTH     = pygame.K_e  # Circle button toggles stealth mode

                                   
# Supports CTRL-C to override threads
def _signal_handler(signal, frame):
    frame.f_locals['rover'].close()
    sys.exit(0)

# Try to start OpenCV for video
try:
    import cv2
except:

    cv2 = None

    # Rover subclass for PS3 + OpenCV
class PS3Rover(Rover20):

    def __init__(self):

        # Set up basics
        self.wname = 'Rover 2.0: Hold ESC to quit'
        self.quit = False

        pygame.init()
        # Set up controller using PyGame
        try:
            pygame.display.init()
            pygame.joystick.init()
            self.controller = pygame.joystick.Joystick(0)
            self.controller.init()
            self.controll = True
            print("Using Controller")

        # Use Keyboard
        except:
            # pygame.display.set_mode((600,600),1,16)

            # pygame.display.init()
            self.controll = False
            self.treadFloat = [float(0),float(0)]
            self.treadstep = .5 # float value for rate of change
            self.changer = {
                -1: self.stop,
                119: self.w,   # move forward
                97: self.a,    # move left
                115: self.s,   # move back
                100: self.d,   # move right
                113: self.q,   # toggle lights WIP
                101: self.e,   # toggle night vision WIP
                103: self.g,   # move camera down
                116: self.t,   # move camera up
                27: self.esc,   # close program
            }
            print("Using Keyboard")


         # Defaults on startup: lights off, ordinary camera
        self.lightsAreOn = False
        self.stealthIsOn = False

        # Tracks button-press times for debouncing
        self.lastButtonTim1e = 0

        # Try to create OpenCV named window
        #try:
            #if cv2:
                #cv2.namedWindow(self.wname, cv2.CV_WINDOW_AUTOSIZE)
            #else:
                #pass
        #except:
            #pass

        self.pcmfile = open('rover20.pcm', 'w')
        Rover20.__init__(self)

    # Automagically called by Rover class
    def processAudio(self, pcmsamples, timestamp_10msec):

        for samp in pcmsamples:
            self.pcmfile.write('%d\n' % samp)

    # Automagically called by Rover class
    def processVideo(self, jpegbytes, timestamp_10msec):
        # Update controller events
        if self.controll:
            pygame.event.pump()
            # Toggle lights
            self.lightsAreOn  = self.checkButton(self.lightsAreOn, KEY_LIGHTS, self.turnLightsOn, self.turnLightsOff)

            # Toggle night vision (infrared camera)
            self.stealthIsOn = self.checkButton(self.stealthIsOn, KEY_STEALTH, self.turnStealthOn, self.turnStealthOff)
            # Move camera up/down
            if self.controller.get_button(BUTTON_CAMERA_UP):
                self.moveCameraVertical(1)
            elif self.controller.get_button(BUTTON_CAMERA_DOWN):
                self.moveCameraVertical(-1)
            else:
                self.moveCameraVertical(0)

            # Set treads based on axes
            self.setTreads(self.axis(1), self.axis(3))
        else:
            keyb = cv2.waitKey(1)
            try:
                self.changer[keyb]()
            except:
                self.changer[-1]
            self.setTreads(self.treadFloat[0], self.treadFloat[1])



        """if keyb[pygame.K_ESCAPE]:
                print("donzo")
                self.quit = True

            print(keyb[pygame.K_LSHIFT])
            # Toggle lights
            # print(pygame.key.get_pressed(pygame.K_LSHIFT))
            self.lightsAreOn  = self.checkKey(self.lightsAreOn, KEY_LIGHTS, keyb, self.turnLightsOn, self.turnLightsOff)

            # Toggle night vision (infrared camera)
            self.stealthIsOn = self.checkKey(self.stealthIsOn, KEY_STEALTH, keyb, self.turnStealthOn, self.turnStealthOff)
            # Move camera up/down
            if keyb[KEY_CAMERA_UP]:
                self.moveCameraVertical(1)
            elif keyb[KEY_CAMERA_DOWN]:
                self.moveCameraVertical(-1)
            else:
                self.moveCameraVertical(0)

            # Set treads based on axes
            a = self.WASD(keyb)
            self.setTreads(a[0],a[1])"""
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

    def a(self):
        if self.treadFloat[0] > -1.0+self.treadstep:
            self.treadFloat[0] -= 2 * self.treadstep
        elif self.treadFloat[0] == -1.0+self.treadstep:
            self.treadFloat[0] -= self.treadstep

        if self.treadFloat[1] < 1.0-self.treadstep:
            self.treadFloat[1] += 2 * self.treadstep
        elif self.treadFloat[1] == 1.0-self.treadstep:
            self.treadFloat[1] += self.treadstep
        self.moveCameraVertical(0)

    def w(self):
        if self.treadFloat[0] < 1.0 - self.treadstep:
            self.treadFloat[0] += 2 * self.treadstep
        elif self.treadFloat[0] == 1.0 - self.treadstep:
            self.treadFloat[0] += self.treadstep

        if self.treadFloat[1] < 1.0 - self.treadstep:
            self.treadFloat[1] += 2 * self.treadstep
        elif self.treadFloat[1] == 1.0 - self.treadstep:
            self.treadFloat[1] += self.treadstep
        self.moveCameraVertical(0)

    def d(self):
        print(self.treadFloat[0], self.treadFloat[1])
        if self.treadFloat[0] < 1.0 - self.treadstep:
            self.treadFloat[0] += 2 * self.treadstep
        elif self.treadFloat[0] == 1.0 - self.treadstep:
            self.treadFloat[0] += self.treadstep

        if self.treadFloat[1] > -1.0 + self.treadstep:
            self.treadFloat[1] -= 2 * self.treadstep
        elif self.treadFloat[1] == -1.0 + self.treadstep:
            self.treadFloat[1] -= self.treadstep
        self.moveCameraVertical(0)

    def s(self):
        if self.treadFloat[0] > -1.0 + self.treadstep:
            self.treadFloat[0] -= 2 * self.treadstep
        elif self.treadFloat[0] == -1.0 + self.treadstep:
            self.treadFloat[0] -= self.treadstep

        if self.treadFloat[1] > -1.0 + self.treadstep:
            self.treadFloat[1] -= 2 * self.treadstep
        elif self.treadFloat[1] == -1.0 + self.treadstep:
            self.treadFloat[1] -= self.treadstep
        self.moveCameraVertical(0)

    def e(self):
        # Toggle night vision (infrared camera)
        print("e has been called")
        if self.stealthIsOn == False:
            self.turnStealthOn()
            self.stealthIsOn = True
        elif self.stealthIsOn == True:
            self.turnStealthOff()
            self.stealthIsOn = False
        print("e, should toggle night vision")

    def q(self):
        print("q has been called")
        if self.lightsAreOn == False:
            self.turnLightsOn()
            self.lightsAreOn = True
        elif self.lightsAreOn == True:
            self.turnLightsOff()
            self.lightsAreOn = False
        print("q, toggle lights")

    def g(self):
        self.moveCameraVertical(-1)
        print("g, moving camera down")

    def t(self):
        self.moveCameraVertical(1)
        print("t, moving camera up")

    def esc(self): #Closes program
        print("Closing Program")
        rover.turnLightsOff()
        rover.lightsAreOn = False
        rover.turnStealthOff()
        rover.stealthIsOn = False
        sys.exit()
        

    """def WASD(self, keyb):
        w = 0
        a = 0
        s = 0
        d = 0
        if keyb[pygame.K_w]:
            w = 1
        else:
            w = 0
        if keyb[pygame.K_a]:
            a = 1
        else:
            a = 0
        if keyb[pygame.K_s]:
            s = 1
        else:
            s = 0
        if keyb[pygame.K_d]:
            d = 1
        else:
            d = 0

        wasd = [w,a,s,d]

        if wasd == [0,0,0,0]:
            return 0, 0
        elif wasd == [1,0,0,0] or wasd == [1,1,0,1]:
            return 1, 1
        elif wasd == [1,1,0,0]:
            return 0,1
        elif wasd == [1,0,0,1]:
            return 1,0
        elif wasd == [0,1,0,0]:
            return -1,1
        elif wasd == [0,0,0,1]:
            return 1,-1
        elif wasd == [0,0,1,0]:
            return -1,-1
        elif wasd == [0,1,1,0]:
            return 0,-1
        elif wasd == [0,0,1,1]:
            return -1,0
        else:
            return 0,0"""

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



