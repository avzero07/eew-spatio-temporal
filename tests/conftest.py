import pytest
import tempfile

from est_lib.util.obspy_util import *
from est_lib.dataset.seismic_dataset import CNDataset
from est_lib.dataset.seismic_dataset_new import EQDataset
from obspy import UTCDateTime as dt

# Fixtures

@pytest.fixture(scope="module")
def temp_dir():
    '''
    Fixture to create a temp_dir for test activities.
    '''
    #TODO: Scope session?
    with tempfile.TemporaryDirectory() as tempdir:
        curr_dir = os.getcwd()
        yield tempdir
        # Precaution before cleanup
        os.chdir(curr_dir)

@pytest.fixture(scope="module")
def sample_inventory():
    inv = inventory_retriever(network="CN",
                              sta_list=['QEPB','HOPB'],
                              level='response')
    yield inv

@pytest.fixture(scope="module")
def sample_inventory_file(temp_dir,sample_inventory):
    f_path = os.path.join(temp_dir,"inv.xml")
    op_file_path = inventory_writer(sample_inventory,
                                    f_path,
                                    file_format="STATIONXML")
    yield op_file_path

@pytest.fixture(scope="module")
def sample_stream():
    stream = stream_retriever(event_time = dt('2021-05-26T08:46:00'),
                              seconds_before = 600,
                              seconds_after = 1500,
                              network="CN",
                              sta_list=['QEPB','HOPB'],
                              channel_list=['HHE','HHN','HHZ'])
    yield stream

@pytest.fixture(scope="module")
def sample_stream_file(temp_dir,sample_stream):
    f_path = os.path.join(temp_dir,"stream.pkl")
    op_file_path = stream_writer(sample_stream,
                                 f_path,
                                 file_format="PICKLE")
    yield op_file_path

@pytest.fixture(scope="module")
def sample_eq_stream_file(sample_stream,sample_inventory,temp_dir):
    sta_list = ['QEPB','HOPB']
    chan_list = ['HHE','HHN','HHZ']
    f_path = os.path.join(temp_dir,"stream.npy")
    op_file_path = stream_data_writer(sample_stream,
                                      sample_inventory,
                                      f_path,
                                      sta_list,
                                      chan_list)
    yield op_file_path

@pytest.fixture(scope="module")
def sample_dataset(sample_inventory_file,sample_stream_file):
    obj = CNDataset(sample_inventory_file,
                    sample_stream_file,
                    sta_list=['HOPB','QEPB'],
                    ip_dim=3,
                    num_nodes=2,
                    seq_length=100)
    yield obj

@pytest.fixture(scope="module")
def sample_eq_dataset(sample_inventory_file,sample_eq_stream_file):
    obj = EQDataset(sample_inventory_file,
                    sample_eq_stream_file,
                    sample_eq_stream_file,
                    sta_list=['HOPB','QEPB'],
                    ip_dim=3,
                    num_nodes=2,
                    seq_length=500)
    yield obj
