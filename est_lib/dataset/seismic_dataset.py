import os
import numpy as np
import torch
from est_lib.util.obspy_util import inventory_reader, stream_reader

class CNDataset(torch.utils.data.Dataset):
    '''
    Dataset of Time Series Seismic Data from CNSN Stations
    '''
    # TODO: Current implementation will assume a single stream.
    def __init__(self,inv_file,stream_file,sta_list,
                 chan_list=['HHE','HHN','HHZ'],ip_dim=3,num_nodes=3,
                 seq_length=100):
        self.stream = stream_reader(stream_file,file_format="PICKLE")
        self.inv = inventory_reader(inv_file)
        self.sta_list = sorted(sta_list) # Important for storage
        self.chan_list = chan_list
        self.ip_dim = ip_dim
        self.num_nodes = num_nodes
        self.seq_length = seq_length
        self.data = None
        self.labels = None

        self._transform_stream()
        self._generate_labels()

    def __len__(self):
        '''
        Returns length along sequence axis
        '''
        trace_len = self.data.shape[2]
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
        data = self.data[:,:,idx:idx+self.seq_length-1]
        label = self.labels[:,:,idx]
        return (data,label)

    def _transform_stream(self):
        '''
        Transform Input Data into torch tensor of form
        num_inp x nodes x seq_length
        '''
        for i,station in enumerate(self.sta_list):
            # TODO: derive sta_list or sort it
            temp_inv = self.inv.select(station=station)
            temp_stream = self.stream.select(station=station)
            # Remove Response #TODO Locate in a better place
            temp_stream.remove_response(inventory=temp_inv)
            # Create a shell for Data the First Time
            if self.data == None:
                '''
                It is necessary to explicitly set precision to
                float64

                use torch.as_tensor instead of torch.tensor
                https://github.com/pytorch/text/issues/467
                https://github.com/pytorch/pytorch/issues/16627
                '''
                self.data = torch.as_tensor(torch.zeros(self.ip_dim,self.num_nodes,
                                        len(temp_stream[0])),
                                        dtype=torch.float64)
            # Copy Data Over
            for j,trace in enumerate(temp_stream):
                self.data[j,i,:] = torch.tensor(trace.data,
                                                dtype=torch.float64)

    def _generate_labels(self):
        '''
        Generate Labels
        '''
        # TODO: Separate Sequence Length and Horizon!
        if self.labels == None:
            self.labels = self.data[:,:,self.seq_length:]

class DatasetError(Exception):
    def __init__(self,message="Problem loading data!"):
        self.message = message
        super().__init__(self.message)
