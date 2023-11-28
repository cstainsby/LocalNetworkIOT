from datetime import datetime
import datetime
from typing import List

from .device_checkout import DeviceCheckout

class Device():
    '''
    This Device object is used to represent a generic object which is usable within the larger 
    piserver project. Each device will need a WiFi connection to communicate with the server so
    that will be assumed.

    This implementation will be used as a state storage tool to easily store and make common operations
    on data loaded from the database. The intention will be to simplify 
    '''
    def __init__(self) -> None:
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
        self.name = ""
        self.mac_address = ""
        self.type = ""
        self.desc = ""
        self.github_link = None

        self.checkouts: List[DeviceCheckout] = [] # instances where the device has been used
    


    def inflate_from_sqlLite_dict(self, data: dict):
        self.mac_address = data["mac_address"]
        self.name = data["name"]
        self.type = data["type"]
        self.desc = data["desc"]
        self.github_link = data["github_link"] if "github_link" in data else None

        if "checkouts" in data:
            raw_checkouts = data["checkouts"]
            formated_checkout = DeviceCheckout()
            formated_checkout.inflate_from_sqlLite_dict(raw_checkouts)
    
    def to_template_data_format(self) -> dict:
        template_data = {
            "name": self.name,
            "mac_address": self.mac_address,
            "desc": self.desc,
            "type": self.type
        }
        if self.github_link:
            template_data["github_link"] = self.github_link

        return template_data
