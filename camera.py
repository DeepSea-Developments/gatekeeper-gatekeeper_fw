import sys
sys.path.insert(1, '../')
from threading import Thread, Semaphore
from queue import Queue
import time

import io
import fcntl
import struct
import time

# The person sensor has the I2C ID of hex 62, or decimal 98.
PERSON_SENSOR_I2C_ADDRESS = 0x62

# We will be reading raw bytes over I2C, and we'll need to decode them into
# data structures. These strings define the format used for the decoding, and
# are derived from the layouts defined in the developer guide.
PERSON_SENSOR_I2C_HEADER_FORMAT = "BBH"
PERSON_SENSOR_I2C_HEADER_BYTE_COUNT = struct.calcsize(PERSON_SENSOR_I2C_HEADER_FORMAT)

PERSON_SENSOR_FACE_FORMAT = "BBBBBBbB"
PERSON_SENSOR_FACE_BYTE_COUNT = struct.calcsize(PERSON_SENSOR_FACE_FORMAT)

PERSON_SENSOR_FACE_MAX = 4
PERSON_SENSOR_RESULT_FORMAT = PERSON_SENSOR_I2C_HEADER_FORMAT + "B" + PERSON_SENSOR_FACE_FORMAT * PERSON_SENSOR_FACE_MAX + "H"
PERSON_SENSOR_RESULT_BYTE_COUNT = struct.calcsize(PERSON_SENSOR_RESULT_FORMAT)

# I2C channel 1 is connected to the GPIO pins
I2C_CHANNEL = 1
I2C_PERIPHERAL = 0x703

# How long to pause between sensor polls.
PERSON_SENSOR_DELAY = 0.2

class camera(Thread):
  def __init__(self, faceQueue):
    self.faceQueue = faceQueue
    self.i2c_handle = io.open("/dev/i2c-" + str(I2C_CHANNEL), "rb", buffering=0)
    fcntl.ioctl(self.i2c_handle, I2C_PERIPHERAL, PERSON_SENSOR_I2C_ADDRESS)
    Thread.__init__(self) 

  def run(self):
    while True:
      try:
        read_bytes = self.i2c_handle.read(PERSON_SENSOR_RESULT_BYTE_COUNT)
      except OSError as error:
        print("No person sensor data found")
        print(error)
        time.sleep(PERSON_SENSOR_DELAY)
        continue
      offset = 0
      (pad1, pad2, payload_bytes) = struct.unpack_from(
          PERSON_SENSOR_I2C_HEADER_FORMAT, read_bytes, offset)
      offset = offset + PERSON_SENSOR_I2C_HEADER_BYTE_COUNT

      (num_faces) = struct.unpack_from("B", read_bytes, offset)
      num_faces = int(num_faces[0])
      offset = offset + 1

      faces = []
      for i in range(num_faces):
        (box_confidence, box_left, box_top, box_right, box_bottom, id_confidence, id,
        is_facing) = struct.unpack_from(PERSON_SENSOR_FACE_FORMAT, read_bytes, offset)
        offset = offset + PERSON_SENSOR_FACE_BYTE_COUNT
        face = {
          "box_confidence": box_confidence,
          "coordinate top": (box_left, box_top),
          "coordinate bottom": (box_right, box_bottom),
          "id_confidence": id_confidence,
          "id": id,
          "is_facing": is_facing,
        }
        faces.append(face)
            
      checksum = struct.unpack_from("H", read_bytes, offset)
      if (num_faces >= 1):
        print(num_faces, faces)
        face_center = [ box_left + (box_right - box_left), box_top+(box_bottom - box_top) ]
        
        if( face_center[0] < 134): #the face is upper, so move the camera upward
          if( 120 < face_center[0]):
            print("horizontal aligned")
          else:
            print("move camera upward")
        else:
          print("move camera downward")
          
        if( face_center[1] < 134):
          if( 120 < face_center[1] ):
            print("vertically aligned")
          else:
            print("move camera to the right")
        else:
          print("move camera to the left")
                      
      time.sleep(PERSON_SENSOR_DELAY)