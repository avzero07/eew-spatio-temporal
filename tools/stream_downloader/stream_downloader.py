'''
Script to download stream files
'''

import os
import sys
import configparser
config = configparser.ConfigParser()
config.read('stream_downloader.ini')
import concurrent.futures
import time
import logging
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
from est_lib.util.obspy_util import *
from est_lib.util.event_parse import *
from itertools import repeat
from tqdm import tqdm

def main(args):
    if len(args) > 0:
        print("Error! Do not Pass any Arguments!",file=sys.stderr)
        sys.exit(1)

    # Read and Load Configs
    dl_root =  os.path.abspath(config['location']['dl_root'])
    sta_list = sorted(config['parameters']['stations'].split(','))
    cha_list = sorted(config['parameters']['channels'].split(','))
    event_list_path = config['parameters']['event_list']
    workers = int(config['parameters']['worker_threads'])
    event_list = Eq_Events(event_list_path)

    # Folder Prep
    curr_dir = os.listdir(dl_root)
    for sta in sta_list:
        if(sta in curr_dir):
            continue
        else:
            os.mkdir(os.path.join(dl_root,sta))

    # Run Parallel Download
    for sta in sta_list:
        # Pre-Filter Event List
        # TODO: Write a new reduced event list to DL root
        inv = inventory_retriever(sta_list=[sta])
        event_membership = Event_Membership(event_list,[sta],cha_list,
                        inventory=inv)
        reduced_event_list = event_membership.find_overlapping_events(cha_list)

        # Set Up Logging
        log_file = os.path.join(dl_root,sta,
                    '{}_download.log'.format(sta))
        logger_name = "{}_logger".format(sta)
        logger = setup_logger(logger_name,log_file,level=logging.DEBUG)
        # Multi Threaded Download
        futures_list = []
        message = "Starting Downloads for {}".format(sta)
        logger.debug(message)
        print(message)
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            logger.debug("Submitting Download Jobs to Workers")
            for i,args in tqdm(enumerate(zip(repeat(sta),reduced_event_list))):
                futures = executor.submit(download_stream,
                        args[0],args[1])
                futures_list.append(futures)
                # Introduce Delay Between Connections
                time.sleep(0.25)
            logger.debug("Waiting for Worker Completion")
            for futures in tqdm(futures_list):
                result = futures.result(timeout=10)
                logger.info(result)
        final_message = ("Completed Processing {} Events for "
                            "{}".format(i+1,sta))
        logger.info(final_message)
        print(final_message)
    sys.exit(0)

def download_stream(sta,event):
    dl_root = config['location']['dl_root']
    dl_root = os.path.abspath(dl_root)
    sta_list = sta
    cha_list = sorted(config['parameters']['channels'].split(','))
    sb = int(config['parameters']['seconds_before'])
    sa = int(config['parameters']['seconds_after'])

    try:
        stream = stream_retriever(event_time=event.Time,
                time_format='string',seconds_before=sb,
                seconds_after=sa,sta_list=[sta],
                channel_list=cha_list)
        f_path = os.path.join(dl_root,sta,
                '{}_{}.mseed'.format(event.Index,sta))
        op_path = stream_writer(stream,f_path)
        return "Download Complete: {}".format(op_path)

    except obspy.clients.fdsn.header.FDSNNoDataException:
        return "No Data Available for {} during Event {}".format(sta,
                event.Index)

def setup_logger(logger_name,log_file,level=logging.INFO):
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

if __name__ == "__main__":
    main(sys.argv[1:])
