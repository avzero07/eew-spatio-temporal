'''
Contains utility functions to interact with obspy.
'''

import numpy as np
import os
import obspy
from obspy.clients.fdsn import Client
client = Client('IRIS')

# Methods to Retrieve Data from IRIS
def inventory_retriever(network='CN',
                        sta_list=None,
                        level='response'):
    '''
    Argument Type
    =============
    - network         : Seismic Station Network ID | default = 'CN' for CNSN
    - sta_list        : List of Station ID Strings eg: ['BFSB','QEPB','HOLB']
    - level           : Level of Information To be Returned | default = 'response'

    Return Type
    ===========
    - inventory       : obspy.core.inventory.inventory.Inventory with
                        details about specified station
    '''
    sta_list_string = stringify_list(sta_list)
    inventory = client.get_stations(network=network,
                                    station=sta_list_string,
                                    level=level)
    return inventory

def stream_retriever(event_time=None,
                     seconds_before=600,
                     seconds_after=1500,
                     network='CN',
                     sta_list=None,
                     channel_list=['HHE','HHN','HHZ'],
                     client_obj=client):
    '''
    Argument Type
    =============
    - event_time      : obspy.UTCDateTime Object Denoting EQ Origin Time
    - seconds_before  : Denotes range start, ie seconds before
                        event_time | default = 600 seconds
    - seconds_after   : Denotes range end  , ie seconds after
                        event_time | default = 1500 seconds
    - network         : Seismic Station Network ID | default = 'CN' for CNSN
    - sta_list        : List of Station ID Strings eg: ['BFSB','QEPB','HOLB']
    - channel_list    : List of Channel ID strings of Interest
                        | default = ['HHE','HHN','HHZ']
    - client_obj      : obspy.clients.fdsn.Client Object
                        | default = obspy.clients.fdsn.Client('IRIS')

    Return Type
    ===========
    - stream          : obspy.core.stream.Stream Object Containing
                        Waveforms from Specific Stations
    '''
    sta_list_string = stringify_list(sta_list)
    channel_string = stringify_list(channel_list)

    t1 = event_time - seconds_before
    t2 = t1 + seconds_after
    if client_obj!=None:
        stream = client.get_waveforms("CN",
                          sta_list_string,
                          location="",
                          starttime=t1,
                          endtime=t2,
                          channel=channel_string)
    else:
        raise ValueError("No Client Object Specified!")
    return stream

# Methods to Write Retrieved Data into Files

def inventory_writer(inventory_obj,file_path,file_format="STATIONXML"):
    '''
    Writes an inventory object into a file in the filesystem.

    Argument Type
    =============
    - inventory_obj     : obspy.core.inventory.inventory.Inventory
                          Object which contains station metadata
    - file_path         : path to target, last part of the path will
                          denote the filename
    - file_format       : denotes the format used by obspy to save
                          data. Default is "STATIONXML" refer to obspy
                          documentation for other supported types.

    Return Type
    ===========
    - f_path            : Returns Path to the Created File
    '''
    f_path = os.path.abspath(file_path)
    inventory_obj.write(f_path,format=file_format)
    return f_path

def stream_writer(stream_obj,file_path,file_format="MSEED"):
    '''
    Writes a stream object into a file in the filesystem.

    Argument Type
    =============
    - stream_obj        : obspy.core.stream.Stream Object which
                          contains one or more seismic traces.
    - file_path         : path to target, last part of the path will
                          denote the filename
    - file_format       : denotes the format used by obspy to save
                          data. Default is "MSEED" refer to obspy
                          documentation for other supported types.

    Return Type
    ===========
    - f_path            : Returns Path to the Created File
    '''
    f_path = os.path.abspath(file_path)
    stream_obj.write(f_path,format=file_format)
    return f_path

def stream_data_writer(stream_obj,inv_obj,filepath,sta_list,
                       chan_list):
    '''
    Writes stream data into a csv file in the files system.

    Data stored as sequence x station x channel
    '''
    sta_list.sort()
    chan_list.sort()

    seq_length = len(stream_obj[0].data)
    node_length = len(sta_list)
    channel_length = len(chan_list)

    filler = np.zeros([seq_length,node_length,channel_length])

    for i,sta in enumerate(sta_list):
        for j,chan in enumerate(chan_list):
            temp = stream_obj.select(station=sta,
                                     channel=chan)
            '''
            This try block is an unfortunate consquence
            of how IRIS data is. I noticed that some
            events had emtpy trace objects within a stream
            list.

            Example,

            1 Trace(s) in Stream:
            CN.CBB..HNZ | 2018-10-22T06:12:45.000000Z -
                    2018-10-22T06:42:45.000000Z | 100.0 Hz, 180001 samples
            0 Trace(s) in Stream:

            0 Trace(s) in Stream:

            0 Trace(s) in Stream:

            1 Trace(s) in Stream:
            CN.HOLB..HNE | 2018-10-22T06:12:45.000000Z -
                    2018-10-22T06:42:45.000000Z | 100.0 Hz, 180001 samples
            1 Trace(s) in Stream:
            CN.HOLB..HNN | 2018-10-22T06:12:45.000000Z -
                    2018-10-22T06:42:45.000000Z | 100.0 Hz, 180001 samples


            '''
            filler[:,i,j] = temp[0].data

    with open(filepath,'wb') as f:
        np.save(f,filler)
    return filepath

def stream_data_reader(filepath):
    '''
    Reads data stored by stream_data_writer and returns
    a numpy array.
    '''
    with open(filepath,'rb') as f:
        return np.load(f,allow_pickle=True)

# Methods to Read Data from Filesystem

def inventory_reader(file_path,file_format="STATIONXML"):
    '''
    Reads inventory data from the file system and returns an inventory
    object.

    Argument Type
    =============
    - file_path         : path to file
    - file_format       : denotes the way the file contents are
                          stored. default is "STATIONXML". Refer to
                          obspy documentation for other supported
                          formats.

    Return Type
    ===========
    - inventory_object  : obspy.core.inventory.inventory.Inventory
                          object.
    '''
    f_path = os.path.abspath(file_path)
    inventory_obj = obspy.read_inventory(f_path,format=file_format)
    return inventory_obj

def stream_reader(file_path,file_format="MSEED"):
    '''
    Reads stream data from the file system and returns a stream
    object.

    Argument Type
    =============
    - file_path         : path to file
    - file_format       : denotes the way the file contents are
                          stored. default is "MSEED". Refer to
                          obspy documentation for other supported
                          formats.

    Return Type
    ===========
    - stream_object     : obspy.core.stream.Stream Object
    '''
    f_path = os.path.abspath(file_path)
    stream_obj = obspy.read(f_path,format=file_format)
    return stream_obj

# Helper Methods

def stringify_list(ip_list,separator=','):
    if len(ip_list)<=1:
        string = ''.join(ip_list)
    else:
        string = separator.join(ip_list)
    return string
