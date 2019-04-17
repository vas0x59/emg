from pandas import DataFrame
import pandas as pd
class Data:
    def __init__(self, template):
        self.__data = {}
        self.columns = []
        
        for i in template:
            # print(len(template[i]))
            if len(template[i]) > 1:
                for j in range(template[i][0]):
                    for y in range(template[i][1]):
                        self.columns.append(i + str(j) + "_" + str(y))
            else:
                for j in range(template[i][0]):
                    self.columns.append(i+ "_" + str(j))

        self.df = DataFrame([[0 for i in self.columns]], columns = self.columns)
    def updateData(self, col, data):
        self.df[col] = data
