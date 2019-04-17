from ArduinoReader import ArduinoReader
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation as animation
import threading
from pandas import DataFrame
import pandas as pd
from Ampl import Ampl
from MedianArray import MedianArray
from PrevValues import PrevValues
from MinMaxValues import MinMaxValues
from Data import Data

from RegCatboost import RegCatboost
rc = RegCatboost('model_4_dima')
ar = ArduinoReader("/dev/ttyACM1")

ar.start()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

reg = False
save = False

cc = ['unixtime', 'emg0', 'emg1', 'emg2', 'emg0_ampl', 'emg1_ampl', 'emg2_ampl', 'emg0_med', 'emg1_med',]

df = DataFrame([[0 for i in cc]], columns = cc)

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

ampls = [Ampl(30) for i in range(3)]
meds = [MedianArray(30) for i in range(3)]
prev_vals = [PrevValues(20) for i in range(3)]
min_max_vals = [MinMaxValues(20) for i in range(3)]
d = Data({'emg':[3], 'emg_ampl':[3], 'emg_med':[3], 'emg_min':[3], 'emg_max':[3], 'emg_prev':[3, 20]})
# Set up plot to call animate() function periodically
def up():
    global df
    global save
    global reg
    while True:
        df_p = DataFrame({
                'emg0':[ar.values[0]], 'emg1':[ar.values[1]], 'emg2':[ar.values[2]],
                'emg0_ampl':[emg0_ampl.calc(ar.values[0])], 'emg1_ampl':[emg1_ampl.calc(ar.values[1])],
                'emg0_med':[emg0_med.calc(ar.values[0])], 'emg1_med':[emg1_med.calc(ar.values[1])], 
                'emg2_ampl':[emg2_ampl.calc(ar.values[2])]})
        print(rc.predict(df_p))
        if reg: 
            df = df.append({'unixtime': time.time(), 
                'emg0':ar.values[0], 'emg1':ar.values[1], 'emg2':ar.values[2],
                'emg0_ampl':emg0_ampl.calc(ar.values[0]), 'emg1_ampl':emg1_ampl.calc(ar.values[1]),
                'emg0_med':emg0_med.calc(ar.values[0]), 'emg1_med':emg1_med.calc(ar.values[1]), 
                'emg2_ampl':emg2_ampl.calc(ar.values[2])}, ignore_index=True)
            print(df)
        if save:
            df.to_csv('./3_sen_dima' + str(int(time.time())) +'.csv')
            df = DataFrame([], columns = cc)
            save = False
        
        time.sleep(0.05)

t = threading.Thread(target=up, args=())
t.daemon = True
t.start()
fig.canvas.mpl_connect('key_press_event', press)
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=25)
plt.show()
