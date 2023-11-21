from datetime import datetime
import datetime

class Device():
    '''
    This Device object is used to represent a generic object which is usable within the larger 
    piserver project. Each device will need a WiFi connection to communicate with the server so
    that will be assumed.

    This implementation will be used as a state storage tool to easily store and make common operations
    on data loaded from the database. The intention will be to simplify 
    '''
    def __init__(self, device_data: dict) -> None:
        '''
        Expected input example:
        {
            mac_address: TEXT NOT NULL,
            device_name: TEXT NOT NULL,
            device_type: TEXT NOT NULL,
            device_desc: TEXT NOT NULL,
            github_link: TEXT
        }
        '''
        self.device_name = device_data["device_name"]
        self.mac_address = device_data["mac_address"]
        self.device_type = device_data["device_type"]
        self.device_desc = device_data["device_desc"]
        self.github_link = device_data["github_link"]