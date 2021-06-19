import pandas as pd

'''
Eq_Events is a wrapper custom container for storing event info read
from a csv file.

__init__ first imports the csv into a pandas dataframe and then
iterates through it to populate a list of named tuples.

The class implements all methods necessary to effectively have it
behave like a container.
'''

class Eq_Events:
    def __init__(self,path_to_event_csv):
        self.df = pd.read_csv(path_to_event_csv,sep='|')
        self.data = list()
        for row in self.df.itertuples():
            self.data.append(row)

    def __getitem__(self,idx):
        if idx > len(self)-1:
            raise IndexError
        return self.data[idx]

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        if self.data is not None:
            return self.data.__iter__()
