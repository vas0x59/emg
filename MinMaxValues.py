class MinMaxValues:
    def __init__(self, window, st_val):
        self.window = window
        self.__arr = [st_val for i in range(window)]
    def append(self, x):
        self.__arr.append(x)
        self.__arr = self.__arr[-self.window: ]
    def getMax(self):
        return max(self.__arr[i])
    def getMin(self):
        return min(self.__arr[i])