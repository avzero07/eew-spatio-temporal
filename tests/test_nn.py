import pytest
import tempfile
import torch
import numpy as np

from est_lib.nn.cp_line_simple import cp_line_simple
from est_lib.util.obspy_util import *
from est_lib.dataset.seismic_dataset import CNDataset
from obspy import UTCDateTime as dt
from obspy.core.util.testing import streams_almost_equal as streq

def test_nn_init():
    net = cp_line_simple()

@pytest.mark.parametrize(
        "ip",
        [((1,1)),
         ((2,1)),
         ((2,2)),
         ((2,3))])
def test_nn_init_param(ip):
    net = cp_line_simple(num_in_nodes=ip[0],feat_size=ip[1])
    assert len(net.lstms) == ip[0], "Wrong number of LSTMS"
    for layer in net.op:
        if len(ip) == 3:
            assert layer.weight.shape[1] == ip[2], "Wrong Number of Hidden Neurons" 
        else:
            assert layer.weight.shape[1] == 3, "Wrong Number of Hidden  Neurons"
        assert layer.weight.shape[0] == 1, "Wrong Number of Outputs"

    for layer in net.hidden:
        assert layer.weight.shape[0] == net.hidden_size, "Mismatch - hidden layer"
        assert layer.weight.shape[1] == ip[0], "Mismatch - dense input"

@pytest.mark.parametrize(
        "ip",
        [(([1,10,3,3])),
         (([2,1,1,1])),
         (([1,5,2,1])),
         (([1,7,2,3])),
         (([4,20,20,3])),
         ])
def test_nn_forward(ip):
    dat = gen_rand_tensor(ip)
    net = cp_line_simple(num_in_nodes=ip[2],
                         feat_size=ip[3])
    op = net(dat)
    for i in range(ip[-1]):
        print(op[i].shape)


# Helper Random Tensor Input
def gen_rand_tensor(dim=[1,1,1,1]):
    return torch.rand(dim)
