import sys
sys.path.insert(1, '../')
from threading import Thread, Semaphore
from queue import Queue
import time
import gpiozero as gpio

PIN_DIRECTION_M1 = 17
PIN_STEP_M1 = 27
PIN_EN_M1 = 22

PIN_DIRECTION_M2 = 24
PIN_STEP_M2 = 23
PIN_EN_M2 = 25

PIN_DIRECTION_M3 = 8
PIN_STEP_M3 = 7
PIN_EN_M3 = 1

SPEED = 0.0008


class control(Thread):
  def __init__(self, commandQueue, faceQueue):
    self.commandQueue = commandQueue
    self.faceQueue = faceQueue      
    
    self.Dir_1 = gpio.LED(PIN_DIRECTION_M1)
    self.Step_1 = gpio.LED(PIN_STEP_M1)  
    self.enable_1 = gpio.LED(PIN_EN_M1)
    self.Dir_2 = gpio.LED(PIN_DIRECTION_M2)  
    self.Step_2 = gpio.LED(PIN_STEP_M2) 
    self.enable_2 = gpio.LED(PIN_EN_M2)
    self.Dir_3 = gpio.LED(PIN_DIRECTION_M3)  
    self.Step_3 = gpio.LED(PIN_STEP_M3) 
    self.enable_3 = gpio.LED(PIN_EN_M3)
    Thread.__init__(self) 
    
  #M1 is left and right movement
  def step_M1(self, speed):
      self.Step_1.on()
      time.sleep(speed)
      self.Step_1.off()
      time.sleep(speed)
        
  def moveLeft(self, speed):
      self.Dir_1.on()
      self.step_M1(speed)
  
  def moveRight(self, speed):
      self.Dir_1.off()
      self.step_M1(speed)
  
  #M2 is up and down movement
  def step_M2(self, speed):
      self.Step_2.on()
      time.sleep(speed)
      self.Step_2.off()
      time.sleep(speed)
      
  def moveUp(self, speed):
      self.Dir_2.on()
      self.step_M2(speed)
  
  def moveDown(self, speed):
      self.Dir_2.off()
      self.step_M2(speed)
      
  #M3 is out and in movement
  def step_M3(self, speed):
      self.Step_3.on()
      time.sleep(speed)
      self.Step_3.off()
      time.sleep(speed)
  
  def moveOut(self, speed):
      self.Dir_3.on()
      self.step_M3(speed)
  
  def moveIn(self, speed):
      self.Dir_3.off()
      self.step_M3(speed)
      
  def putOut(self):
      self.enable_3.off()
      for i in range(1000):  
          self.moveIn(0.0005)
      time.sleep(1)
      for i in range(1000): 
          self.moveOut(0.0005)
      

  def run(self):
      while True:
        if not self.commandQueue.empty():
          command, step, speed = self.commandQueue.get()
          if command == 'p':
            self.enable_3.off()
            self.putOut()
          else: 
            self.enable_1.off()
            self.enable_2.off()
            for i in range(step):  
              if command == "left" or  command == 'l':
                self.moveLeft(speed)
              if command == "right" or command == 'r':
                self.moveRight(speed)
              if command == "up" or command == 'u':
                self.moveUp(speed)
              if command == "down" or command == 'd':
                self.moveDown(speed)
        self.enable_1.on()
        self.enable_2.on()
        self.enable_3.on()
        time.sleep(0.0001)