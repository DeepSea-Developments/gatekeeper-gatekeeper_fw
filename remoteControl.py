import sys
sys.path.insert(1, '../')
from threading import Thread, Semaphore
from queue import Queue
#import pygame
#from pygame.locals import *
import time
import evdev 


class remoteController(Thread):
  def __init__(self, commandQueue):
    self.commandQueue = commandQueue
    #pygame.init()
    self.devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    Thread.__init__(self) 
    
  def run(self):
    self.keyboard = None
    pressed_keys = {}
      
    while True:
      if self.keyboard is None:
        self.devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        for dev in self.devices:
          if dev.name == "Ahuyama Keyboard":
            self.keyboard = dev
            break
      else: 
        for event in self.keyboard.read_loop():
          if event.type == evdev.ecodes.EV_KEY:
            key_event = evdev.categorize(event)
            key_code = key_event.scancode
            
            if key_event.keystate == key_event.key_down:
              key = evdev.ecodes.KEY[event.code]
              print("Tecla presionada:", key)
              pressed_keys[key_code] = True
              if(key == "KEY_ENTER"):
                message = [ "p", 5, 0.001 ] 
                self.commandQueue.put(message)
                
            elif key_event.keystate == key_event.key_up:
              key = evdev.ecodes.KEY[event.code]
              print("Tecla liberada:", key)
              pressed_keys[key_code] = False
              
          for key_code, is_pressed in pressed_keys.items():
            if is_pressed:
              key = evdev.ecodes.KEY[key_code]
              if(key == "KEY_UP"):
                message = [ "u", 10, 0.0008 ]
                #print("Tecla presionada:", key)
                self.commandQueue.put(message)
              elif(key == "KEY_DOWN"):
                message = [ "d", 10, 0.0008 ]
                #print("Tecla presionada:", key)
                self.commandQueue.put(message)
              elif(key == "KEY_LEFT"):
                message = [ "l", 10, 0.0008 ]
                #print("Tecla presionada:", key)
                self.commandQueue.put(message)  
              elif(key == "KEY_RIGHT"):
                message = [ "r", 10, 0.0008 ]
                #print("Tecla presionada:", key)
                self.commandQueue.put(message)
            
      time.sleep(0.0001)