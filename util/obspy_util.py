'''
Contains utility functions to interact with obspy.
'''

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
    - inventory       : obspy.core.inventory.inventory.Inventory with details about specified stations
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
    - seconds_before  : Denotes range start, ie seconds before event_time | default = 600 seconds
    - seconds_after   : Denotes range end  , ie seconds after event_time | default = 1500 seconds
    - network         : Seismic Station Network ID | default = 'CN' for CNSN
    - sta_list        : List of Station ID Strings eg: ['BFSB','QEPB','HOLB']
    - channel_list    : List of Channel ID strings of Interest | default = ['HHE','HHN','HHZ']
    - client_obj      : obspy.clients.fdsn.Client Object | default = obspy.clients.fdsn.Client('IRIS') 

    Return Type
    ===========
    - stream          : obspy.core.stream.Stream Object Containing Waveforms from Specific Stations
    '''
    sta_list_string = stringify_list(sta_list)
    channel_string = stringify_list(channel_list)

    t1 = event_time - (10*60)
    t2 = t1 + (35*60)
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

# Helper Methods

def stringify_list(ip_list,separator=','):
    if len(ip_list)<=1:
        string = ''.join(ip_list)
    else:
        string = srparator.join(ip_list)
    return string
