import pytest
import os

from est_lib.util.event_parse import *
from obspy import UTCDateTime as dt

# Tests

@pytest.fixture(scope="module",autouse=True)
def sample_event_list(temp_dir):
    text =("#EventID|Time|Latitude|Longitude|Depth/km|MagType|Magnitude|EventLocationName\n"
    "20201226.0040001|2020-12-26T00:40:05|48.9638|-128.6807|10.0|Mw|3.5|181"
    "km SW of Port Alice, BC/181 km SO de Port Alice, BC\n"
    "20201222.1141001|2020-12-22T11:41:14|49.2239|-126.824|30.78|ML|2.7|68"
    "km W of Tofino, BC/68 km O de Tofino, BC\n"
    "20201217.1400001|2020-12-17T14:00:57|49.7581|-127.3807|18.7|ML|2.2|70"
    "km S of Port Alice, BC/70 km S de Port Alice, BC\n"
    "20201212.0717001|2020-12-12T07:17:01|50.9757|-129.7843|10.0|Mw|2.8|162"
    "km W of Port Hardy, BC/162 km O de Port Hardy, BC\n"
    "20201209.1947001|2020-12-09T19:47:00|48.7201|-128.8984|10.0|Mw|3.5|212"
    "km SW of Port Alice, BC/212 km SO de Port Alice, BC\n"
    "20201207.1711002|2020-12-07T17:11:11|48.8722|-122.3827|27.24|ML|2.0|23"
    "km SW of Abbotsford, BC/23 km SO de Abbotsford, BC\n"
    "20201206.0802002|2020-12-06T08:02:44|48.0729|-124.6964|41.2|ML|2.0|57"
    "km S of Port Renfrew, BC/57 km S de Port Renfrew, BC\n"
    "20201128.1300002|2020-11-28T13:00:53|50.9848|-124.6304|19.86|ML|2.1|115"
    "km N of Campbell River, BC/115 km N de Campbell River, BC\n"
    "20201128.0811004|2020-11-28T08:11:07|50.9798|-124.6044|19.39|ML|2.3|115"
    "km NE of Campbell River, BC/115 km NE de Campbell River, BC\n")
    f_path = os.path.join(temp_dir,"ev_list.txt")
    with open(f_path,'w') as f:
        f.write(text)
    return f_path

def test_init(sample_event_list):
    obj = Eq_Events(sample_event_list)

def test_len(sample_event_list):
    obj = Eq_Events(sample_event_list)
    assert len(obj) == 9, "Incorrect Length, Expected 9!"

@pytest.mark.parametrize(
        "ip,op",
        [((0,"Magnitude"),3.5),
         ((1,"Time"),"2020-12-22T11:41:14"),
         ((2,"_5"),18.7), # Depth/km treated as _5 (5th header)
         ((3,"Latitude"),50.9757),
         ((4,"Index"),4)])
def test_get_attr(ip,op,sample_event_list):
    obj = Eq_Events(sample_event_list)
    assert op == getattr(obj[ip[0]],ip[1]), "Expected a match!"
    
def test_get_item(sample_event_list):
    obj = Eq_Events(sample_event_list)
    print(obj[0])

def test_iter(sample_event_list):
    obj = Eq_Events(sample_event_list)
    for i,item in enumerate(obj):
        print(item)
    assert i == 8, "Incorrect Final Index, Expected i == 8!"

    assert item == obj[i], "Should be the same!"
