import pytest
import tempfile
import torch
import numpy as np

from est_lib.nn.cp_line_simple import cp_line_simple
from est_lib.util.obspy_util import *
from est_lib.dataset.seismic_dataset import CNDataset
from obspy import UTCDateTime as dt
from obspy.core.util.testing import streams_almost_equal as streq

def test_nn_init(sample_dataset):
    net = cp_line_simple()

def test_nn_forward(sample_dataset):
    obj = sample_dataset
    net = cp_line_simple()
    net(obj.data)

