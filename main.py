from ArduinoReader import ArduinoReader
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation as animation
import threading
from pandas import DataFrame
import pandas as pd

ar = ArduinoReader("/dev/ttyACM1")

ar.start()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

reg = False
save = False

df = DataFrame([], columns = ['unixtime', 'emg0', 'emg1'])

def animate(i, xs, ys):

    xs.append(time.time())
    ys.append(ar.values[0])

    # Limit x and y lists to 20 items
    xs = xs[-100:]
    ys = ys[-100:]

    # Draw x and y lists
    ax.clear()
    plt.ylim((0,1025))
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0)
    
    plt.title('Unixtime')
    plt.ylabel('Markovka')
def press(event):
    global reg
    global save
    print('press', event.key)
    # sys.stdout.flush()
    if event.key == 'x':
        reg = not reg
    if event.key == 'y':
        save = True

# Set up plot to call animate() function periodically
def up():
    global df
    global save
    global reg
    while True:
        print(ar.values, save, reg)
        if reg:
            df = df.append({'unixtime': time.time(), 'emg0':ar.values[0], 'emg1':ar.values[1]}, ignore_index=True)
        if save:
            df.to_csv('./hello_world_from_markovka' + str(int(time.time())) +'.csv')
            df = DataFrame([], columns = ['unixtime', 'emg0', 'emg1'])
            save = False
        time.sleep(0.05)

t = threading.Thread(target=up, args=())
t.daemon = True
t.start()
fig.canvas.mpl_connect('key_press_event', press)
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=25)
plt.show()
