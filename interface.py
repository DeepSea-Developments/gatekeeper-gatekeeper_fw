import sys
sys.path.insert(1, '../')
from threading import Thread, Semaphore
from queue import Queue
import time


class interface(Thread):
    def __init__(self, commandQueue):
      self.commandQueue = commandQueue
      print("Welcome to gatekeeper CLI\n")
      Thread.__init__(self) 
      
    def run(self):
      while True:
        command = input("Enter your command, ie. [left, right, up, down] [steps] [speed] \n").split(" ")
        try:
          if(len(command)==1):
            message = [ command[0], 50, 1 ]
            self.commandQueue.put(message)
          else:
            if(len(command)==3):
              message = [command[0], int(command[1]), float(command[2])]
              self.commandQueue.put(message)
            else:
              print("bad parameters entered, remember type command=steps,speed\n")
        except:
          print("bad command syntax\n")