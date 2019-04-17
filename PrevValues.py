class PrevValues:
  def __init__(self, window, st_val):
    self.window = window
    self.arr = [st_val for i in range(window)]
  def append(self, x):
    self.arr.append(x)
    slef.arr = self.arr[-self.window:]
  def getVal(self, i):
    return self.arr[i]
