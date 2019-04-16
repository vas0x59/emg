import serial
import io
import threading
import time
import numpy as np
class ArduinoReader:
    def __init__(self, url):
        self.ser = serial.Serial(url, 115200, timeout=0)
        self.values = [0, 0, 0]
    def update(self):
        while True:
            line = str(self.ser.readline())
            # print(line[2])
            if line[2] == '$' and line[-6] == '#':
                data = list(map(float, line[3:-6].split(" ")))
                if (len(data) == 3):
                    self.values = data
            time.sleep(0.050)
    
    def start(self):
        t = threading.Thread(target=self.update, args=())
        t.daemon = True
        t.start()