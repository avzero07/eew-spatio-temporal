'''
Script to download stream files
'''

import os
import sys
import configparser
config = configparser.ConfigParser()
config.read('stream_downloader.ini')
import concurrent.futures
import logging
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
from est_lib.util.obspy_util import *
from est_lib.util.event_parse import *
from itertools import repeat

def main(args):
    if len(args) > 0:
        print("Error! Do not Pass any Arguments!",file=sys.stderr)
        sys.exit(1)
    
    # TODO: Add logging statements

    # Read and Load Configs
    dl_root =  os.path.abspath(config['location']['dl_root'])
    sta_list = sorted(config['parameters']['stations'].split(','))
    cha_list = sorted(config['parameters']['channels'].split(','))
    event_list_path = config['parameters']['event_list']
    event_list = Eq_Events(event_list_path)

    # Pre-Filter Event List
    # TODO: Write a new reduced event list to DL root
    inv = inventory_retriever(sta_list=sta_list)
    event_membership = Event_Membership(event_list,sta_list,cha_list,
                    inventory=inv)
    reduced_event_list = event_membership.find_overlapping_events(cha_list)

    # Folder Prep
    curr_dir = os.listdir(dl_root)
    for sta in sta_list:
        if(sta in curr_dir):
            continue
        else:
            os.mkdir(os.path.join(dl_root,sta))

    # Run Parallel Download
    for sta in sta_list:
        futures_list = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
            for args in zip(repeat(sta),reduced_event_list):
                futures = executor.submit(download_stream,
                        args[0],args[1])
                futures_list.append(futures)

            for futures in futures_list:
                result = futures.result(timeout=10)
                print(result)
    sys.exit(0)

def download_stream(sta,event):
    dl_root = config['location']['dl_root']
    dl_root = os.path.abspath(dl_root)
    sta_list = sta
    cha_list = sorted(config['parameters']['channels'].split(','))

    try:
        stream = stream_retriever(event_time=event.Time,
                time_format='string',sta_list=[sta],
                channel_list=cha_list)
        f_path = os.path.join(dl_root,sta,
                '{}_{}.mseed'.format(event.Index,sta))
        op_path = stream_writer(stream,f_path)
        return "Download Complete: {}".format(op_path)

    except obspy.clients.fdsn.header.FDSNNoDataException:
        return "No Data Available for {} during Event {}".format(sta,
                event.Index)

if __name__ == "__main__":
    main(sys.argv[1:])
