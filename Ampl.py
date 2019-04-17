class Ampl:
    def __init__(self, window=20):
        self.arr = [500 for i in range(window)]
        self.window = window
    def update(self, y):
        self.arr.append(y)
        self.arr = self.arr[-self.window:]
        return (max(self.arr) - min(self.arr))

    def getVal(self):
        return (max(self.arr) - min(self.arr))