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

    def inflate_from_sqlLite_row(self, data: list):
        self.mac_address = data[0]
        self.name = data[1]
        self.type = data[2]
        self.desc = data[3]
        self.github_link = data[4] if data[4] != "None" else None
    
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
