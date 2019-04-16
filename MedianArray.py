class MedianArray:
    def __init__(self, window=20):
        self.arr = [0 for i in range(window)]
        self.window = window
    def calc(self, y):
        self.arr.append(y)
        self.arr = self.arr[-self.window:]
        qwe = 0
        for i in self.arr:
            qwe+=i
        return qwe / len(self.arr)