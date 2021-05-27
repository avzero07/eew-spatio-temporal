import pytest
import tempfile
import torch

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
