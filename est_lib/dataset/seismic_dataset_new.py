import os
import numpy as np
import torch
from est_lib.util.obspy_util import inventory_reader, stream_data_reader

class EQDataset(torch.utils.data.Dataset):
    '''
    Dataset of Time Series Seismic Data from CNSN Stations
    '''
    # TODO: Current implementation will assume a single event.
    def __init__(self,inv_file,stream_file,sta_list,
                 chan_list=['HHE','HHN','HHZ'],ip_dim=3,num_nodes=3,
                 seq_length=100):
        self.stream = stream_data_reader(stream_file)
        self.inv = inventory_reader(inv_file)
        self.sta_list = sorted(sta_list) # Important for storage
        self.chan_list = sorted(chan_list)
        self.ip_dim = ip_dim
        self.num_nodes = num_nodes
        self.seq_length = seq_length

    def __len__(self):
        '''
        Returns length along sequence axis
        '''
        trace_len = self.stream.shape[0]
        trace_len_usable = trace_len - self.seq_length
        return trace_len_usable

    def __getitem__(self,idx):
        '''
        Indexed along sequence axis
        '''
        if idx < 0:
            idx = len(self) + idx
        if idx >= len(self):
            raise DatasetError("Trying to read beyond Index!")
        data = torch.Tensor(self.stream[idx:idx+self.seq_length-1,:,:])
        label = torch.Tensor(self.stream[idx+self.seq_length,:,:])
        return (data,label)

class DatasetError(Exception):
    def __init__(self,message="Problem loading data!"):
        self.message = message
        super().__init__(self.message)
