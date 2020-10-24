import pandas as pd

class Dataset():
    def __init__(self):
        self.data = None
        self.df = None
    def load(self, data):
        self.data = data

    def makeDF(self, index = None, columns = None):
        self.df = pd.DataFrame(data=self.data, index=index, columns=columns)
        self.df.drop_duplicates(subset="일자", keep="first")

    def toCSV(self, filename):
        (self.df).to_csv(filename+".CSV")