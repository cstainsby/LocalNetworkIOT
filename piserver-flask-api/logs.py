from datetime import datetime

def log_error():
    pass 

def log_device_status(mac_address: str, time_stamp: str):
    '''
    Create a json log containing information regarding a devices current status

        Metrics will include:
            -battery life
            -connection strength

    '''
    status_log = {
        "mac_address": mac_address,
        "creation_time": time_stamp,
        
    }

def log_device_startup():
    '''
        Create a json log containing information regarding a devices meta information on startup

        Metrics will include:
            -Code version identifier
            -device mac address
    '''
    pass 

def log_device_shutdown():
    pass

