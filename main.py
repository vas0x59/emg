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
rc = RegCatboost('model_8_mark')
ar = ArduinoReader("/dev/ttyACM0")

ar.start()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

reg = False
save = False

# cc = ['unixtime', 'emg0', 'emg1', 'emg2', 'emg0_ampl', 'emg1_ampl', 'emg2_ampl', 'emg0_med', 'emg1_med',]
d = Data({'emg':[3], 'emg_ampl':[3], 'emg_med':[3], 'emg_min':[3], 'emg_max':[3], 'emg_prev':[3, 20]})
cc = d.columns
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
def setEmg(dq, vals):
    for i in range(len(vals)):
        dq.updateData("emg_"+str(i), vals[i])
    return dq

def setEmgObj(dq, vals, su):
    for i in range(len(vals)):
        dq.updateData("emg_" + su + "_" + str(i), vals[i].getVal())
    return dq
def setEmgObj2(dq, vals, su, c):
    for i in range(len(vals)):
        dq.updateData("emg_" + su + "_" + str(i), vals[i].getVal(c))
    return dq
def setEmgObj3(dq, vals, su, c, y):
    for i in range(len(vals)):
        dq.updateData("emg_" + su + "_" + str(i) + "_" + str(y), vals[i].getVal(c))
    return dq
def updateEmgObj(objs, vals):
    for i in range(len(vals)):
        objs[i].update(vals[i])
ampls = [Ampl(45) for i in range(3)]
meds = [MedianArray(45) for i in range(3)]
prev_vals = [PrevValues(20, 500) for i in range(3)]
min_max_vals = [MinMaxValues(20) for i in range(3)]
vals = [500, 500, 500]
# Set up plot to call animate() function periodically
def up():
    global df
    global save
    global reg
    global d
    global vals
    while True:
        # vals = ar.values
        # updateEmgObj(ampls, vals)
        # updateEmgObj(meds, vals)
        # updateEmgObj(prev_vals, vals)
        # updateEmgObj(min_max_vals, vals)
        # time.sleep(0.001)

        d = setEmg(d, vals)
        d = setEmgObj(d, ampls, "ampl")
        d = setEmgObj(d, meds, "med")
        d = setEmgObj2(d, min_max_vals, "min", 0)
        d = setEmgObj2(d, min_max_vals, "max", 1)
        for i in range(20):
            d = setEmgObj3(d, prev_vals, "prev", i, i)
        
        # print(rc.predict(d.df))
        if reg: 
            df = pd.concat([df, d.df], axis=0)
            print(df)
        if save:
            df.to_csv('./3_sen_mark' + str(int(time.time())) +'.csv')
            df = d.df
            save = False
        
        time.sleep(0.001)

def calc():
    global df
    global save
    global reg
    global d
    global vals
    while True:
        vals = ar.values
        updateEmgObj(ampls, vals)
        updateEmgObj(meds, vals)
        updateEmgObj(prev_vals, vals)
        updateEmgObj(min_max_vals, vals)
        time.sleep(0.01)

t2 = threading.Thread(target=calc, args=())
t2.daemon = True
t2.start()

t = threading.Thread(target=up, args=())
t.daemon = True
t.start()
fig.canvas.mpl_connect('key_press_event', press)
# ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=25)
plt.show()
while True:
    pass
