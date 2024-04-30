if __name__ == '__main__':  #main Thread for intercommunication and sync
    #queues creation
    commandQueue = Queue()
    faceQueue = Queue()
    
    #threads init
    cam = camera(faceQueue)
    cam.start()
