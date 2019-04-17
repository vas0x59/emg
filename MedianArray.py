class MedianArray:
    def __init__(self, window=20):
        self.arr = [500 for i in range(window)]
        self.window = window
        self.val = 500
    def update(self, y):
        self.arr.append(y)
        self.arr = self.arr[-self.window:]
        qwe = 0
        for i in self.arr:
            qwe+=i
        self.val = qwe / len(self.arr)
        return self.val
    def getVal(self):
        return self.val