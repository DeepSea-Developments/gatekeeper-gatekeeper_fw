from threading import Thread, Semaphore
from multiprocessing import Queue
from camera import camera
from control import control
if __name__ == '__main__':  #main Thread for intercommunication and sync
    #queues creation
    commandQueue = Queue()
    faceQueue = Queue()
    
    #threads init
    cam = camera(faceQueue)
    cam.start()
    outputs = control(commandQueue, faceQueue)
    outputs.start()
