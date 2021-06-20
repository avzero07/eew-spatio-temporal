import numpy as np
import pandas as pd
from est_lib.util.obspy_util import was_station_active
from tqdm import tqdm

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

'''
Data structure for the membership table. Has as many rows as number of
events. As many columns as stations. Each cell is as deep as the
number of channels.

Stations are assumed to be in alphabetical order. Same with channels.

Row number corresponds to the index value of the event in the
Eq_Events object used to init the Event_Membership object.

The membership table is meant to help create subsets of events that
meet certain criteria. For this project, the main usecase is to
identify events for which all stations have seismic data.

Membership Table Shape
[num_events x num_stations x num_channels]
'''

class Event_Membership:
    def __init__(self,eq_events_object,sta_list,cha_list,
            inventory=None):
        self.eq_events = eq_events_object
        self.num_rows = len(self.eq_events)
        self.sta_list = sorted(sta_list)
        self.num_cols = len(self.sta_list)
        self.cha_list = sorted(cha_list)
        self.num_cha = len(self.cha_list)
        self.table = np.zeros((self.num_rows,self.num_cols,self.num_cha),
                dtype=int)
        if(inventory is not None):
            self.populate_membership_table(inventory)

    def populate_membership_table(self,inventory_object):
        for index,ev in enumerate(tqdm(self.eq_events)):
            time = ev.Time
            for sta in self.sta_list:
                for cha in self.cha_list:
                    val = was_station_active(inventory_object,
                            time,sta,cha)
                    if(val > 0):
                        self.increment_value(ev,sta,cha,val)

    def increment_value(self,event,sta,cha,new_val):
        sta_idx = self.sta_list.index(sta)
        cha_idx = self.cha_list.index(cha)
        self.table[event.Index,sta_idx,cha_idx] = new_val

    def find_overlapping_events(self,cha_list):
        '''
        Returns an event list which is a subset of self.eq_events.data
        which represent events for which we have data from all
        stations.
        '''
        res = list()
        cha_list.sort() #TODO: Validate input vs self.cha_list
        for index,ev in enumerate(tqdm(self.eq_events)):
            count = 0
            for s,sta in enumerate(self.sta_list):
                for c,cha in enumerate(cha_list):
                    if(self.table[index,s,c] == 1):
                        count+=1
            if(count == (self.num_cols*len(cha_list))):
                res.append(ev)
        return res
