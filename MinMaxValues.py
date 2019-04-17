class MinMaxValues:
    def __init__(self, window):
        self.window = window
        self.__arr = [500 for i in range(window)]
    def update(self, x):
        self.__arr.append(x)
        self.__arr = self.__arr[-self.window: ]
    def getMax(self):
        return max(self.__arr)
    def getMin(self):
        return min(self.__arr)

    def getVal(self, c):
        if c == 0:
            return self.getMin()
        elif c == 1:
            return self.getMax()