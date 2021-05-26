import pytest
import tempfile

from est_lib.util.obspy_util import *
from obspy import UTCDateTime as dt
from obspy.core.util.testing import streams_almost_equal as streq

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
def sample_stream():
    stream = stream_retriever(event_time = dt('2021-05-26T08:46:00'),
                              seconds_before = 600,
                              seconds_after = 1500,
                              network="CN",
                              sta_list=['QEPB','HOPB'],
                              channel_list=['HHE','HHN','HHZ'])
    yield stream

# Tests

#TODO: Parametrize
def test_inventory_retriever():
    inv = inventory_retriever(network="CN",
                              sta_list=['QEPB','HOPB'],
                              level='response')
    assert inv != None, "None-type Inventory Returned!"

#TODO: Parametrize
def test_stream_retriever():
    stream = stream_retriever(event_time = dt('2021-05-26T08:46:00'),
                              seconds_before = 600,
                              seconds_after = 1500,
                              network="CN",
                              sta_list=['QEPB','HOPB'],
                              channel_list=['HHE','HHN','HHZ'])
    assert stream != None, "None-type Inventory Returned!"

def test_inventory_writer(temp_dir,sample_inventory):
    op_file = inventory_writer(sample_inventory,
                               os.path.join(temp_dir,'tst_inv.xml'),
                               file_format="STATIONXML")
    print(os.listdir(temp_dir))
    assert os.path.exists(op_file), "tst_inv.xml Not Found in \
                                    {}!".format(temp_dir)

def test_stream_writer(temp_dir,sample_stream):
    op_file = stream_writer(sample_stream,
                            os.path.join(temp_dir,'tst_strm.pkl'),
                            file_format="PICKLE")
    print(os.listdir(temp_dir))
    assert os.path.exists(op_file), "tst_strm.pkl Not Found in \
                                    {}!".format(temp_dir)

def test_inventory_reader(temp_dir,sample_inventory):
    f_path = os.path.join(temp_dir,"tst_inv.xml")
    inv = inventory_reader(f_path,
                           file_format="STATIONXML")
    assert inv == sample_inventory, "Mismatch!"

def test_stream_reader(temp_dir,sample_stream):
    f_path = os.path.join(temp_dir,"tst_strm.pkl")
    stream = stream_reader(f_path,
                           file_format="PICKLE")
    assert streq(stream,sample_stream), "Mismatch!"
