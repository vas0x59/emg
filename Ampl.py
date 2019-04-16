class Ampl:
    def __init__(self, window=20):
        self.arr = [0 for i in range(window)]
        self.window = window
    def calc(self, y):
        self.arr.append(y)
        self.arr = self.arr[-self.window:]
        return (max(self.arr) - min(self.arr))