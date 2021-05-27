import pytest
import tempfile
import torch
import numpy as np

from est_lib.util.obspy_util import *
from est_lib.dataset.seismic_dataset import CNDataset
from obspy import UTCDateTime as dt
from obspy.core.util.testing import streams_almost_equal as streq

def test_datatset_init(sample_inventory_file,sample_stream_file):
    obj = CNDataset(sample_inventory_file,
                    sample_stream_file,
                    sta_list=['HOPB','QEPB'],
                    ip_dim=3,
                    num_nodes=2,
                    seq_length=100)

def test_dataset_len(sample_stream,sample_dataset):
    obj = sample_dataset
    assert len(obj) == len(sample_stream[0])-obj.seq_length,"Usable\
                            Length Mismatch!"

def test_dataset_get_item(sample_inventory,sample_stream,sample_dataset):
    obj = sample_dataset
    assert obj[0] != None, "Error Did not expect empty result!"

    a = obj[-1]
    b = obj[len(obj)-1]
    assert torch.all(a[0].eq(b[0])), "Data Component Note Equal!"
    assert torch.all(a[1].eq(b[1])), "Label Component Equal!"

def test_dataset_stream_content(sample_inventory,sample_stream,sample_dataset):
    obj = sample_dataset

    # Remove Instrument Response
    stream = sample_stream.select()
    stream.remove_response(inventory=sample_inventory)

    # Loop Through Traces
    stat = None
    k = -1
    for i,trace in enumerate(stream):
        tr = torch.tensor(trace.data)
        curr_stat = trace.meta.station
        
        if stat == None:
            stat = trace.meta.station
            k+=1
        
        if stat != curr_stat:
            stat = curr_stat
            k+=1

        if trace.meta.channel == 'HHE':
            j = 0
        elif trace.meta.channel == 'HHN':
            j = 1
        else:
            j = 2
        dt = obj.data[j,k,:]
        # Compare
        '''
        Noticed slight variations in floating point values.
        eg:
        (Pdb) torch.set_printoptions(precision=16)
        (Pdb) print(dt[0]) tensor(-4.0928415501184645e-07)
        (Pdb) print(tr[0]) tensor(-4.0928416076873266e-07, dtype=torch.float64)

        The Zero tensor construct created initially to house stream
        data was initialized to float32. Fixed this to resolve
        discrepancies.
        '''
        assert torch.all(dt.eq(tr)), "Trace Does not match slice!"
