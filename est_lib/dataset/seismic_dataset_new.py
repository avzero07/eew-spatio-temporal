import os
import numpy as np
import torch
from est_lib.util.obspy_util import inventory_reader, stream_data_reader

class EQDataset(torch.utils.data.Dataset):
    '''
    Dataset of Time Series Seismic Data from CNSN Stations
    '''
    # TODO: Current implementation will assume a single event.
    def __init__(self,inv_file,stream_file_data,
                 stream_file_label,sta_list,
                 chan_list=['HHE','HHN','HHZ'],ip_dim=3,num_nodes=3,
                 seq_length=100,horizon=0):
        self.stream_data = torch.Tensor(stream_data_reader(stream_file_data))
        self.stream_data = self.stream_data.to(get_device())
        self.stream_label = torch.Tensor(stream_data_reader(stream_file_label))
        self.stream_label = self.stream_label.to(get_device())
        self.inv = inventory_reader(inv_file)
        self.sta_list = sorted(sta_list) # Important for storage
        self.chan_list = sorted(chan_list)
        self.ip_dim = ip_dim
        self.num_nodes = num_nodes
        self.seq_length = seq_length
        self.horizon = horizon

    def __len__(self):
        '''
        Returns length along sequence axis
        '''
        assert self.stream_data.shape[0] == self.stream_label.shape[0]
        trace_len = self.stream_data.shape[0]
        trace_len_usable = trace_len - self.seq_length - self.horizon
        return trace_len_usable

    def __getitem__(self,idx):
        '''
        Indexed along sequence axis
        '''
        if idx < 0:
            idx = len(self) + idx
        if idx >= len(self):
            raise DatasetError("Trying to read beyond Index!")
        data = self.stream_data[idx:idx+self.seq_length-1,:,:]
        label = self.stream_label[idx+self.seq_length+self.horizon,:,:]
        return (data,label)

class DatasetError(Exception):
    def __init__(self,message="Problem loading data!"):
        self.message = message
        super().__init__(self.message)

# Helper Functions
def get_device():
    if torch.cuda.is_available():
        device = "cuda:0"
    else:
        device = "cpu"
    return device
