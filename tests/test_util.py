import pytest
import tempfile

from est_lib.util.obspy_util import *
from obspy import UTCDateTime as dt
from obspy.core.util.testing import streams_almost_equal as streq

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

def test_stream_data_writer(temp_dir,sample_stream,sample_inventory):
    f_path = os.path.join(temp_dir,'sample.npy')
    stream = sample_stream
    inv = sample_inventory

    op = stream_data_writer(stream,inv,f_path,['QEPB','HOPB'],
                       ['HHE','HHN','HHZ'])

def test_stream_data_reader(temp_dir,sample_stream,sample_inventory):
    f_path = os.path.join(temp_dir,'sample.npy')
    stream = sample_stream
    inv = sample_inventory

    op = stream_data_reader(f_path)

    c = 0
    for st in range(2):
        for ch in range(3):
            assert np.all(np.equal(op[:,st,ch],stream[c].data)), "Mismatch"
            c+=1

@pytest.mark.parametrize(
        "ip,op",
        ([(('2019-12-25T03:36:01.578000Z','QEPB','HHZ'),(0)),
          (('2019-12-25T03:36:01.578000Z','HOPB','HHE'),(1)),
          (('2019-12-25T03:36:01.578000Z','HOPB','HHZ'),(1)),
          (('2019-12-25T03:36:01.578000Z','HOPB','HNZ'),(1)),
          (('2019-12-25T03:36:01.578000Z','QEPB','HNE'),(0)),
          ]))
def test_was_station_active(ip,op,sample_inventory):
    res = was_station_active(sample_inventory,ip[0],ip[1],ip[2])
    assert res == op, "Unexpected Answer!"
