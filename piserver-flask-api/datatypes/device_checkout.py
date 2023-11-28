
from .user import User
from .project import Project

import datetime

class DeviceCheckout():
    def __init__(self) -> None:

        self.mac_address = ""
        self.project_name = ""
        self.start_time = ""
        self.end_time = None
        self.checked_out_to: User = None
        self.checked_device: Project = None

    
    def inflate_from_sqlLite_dict(self, data: dict):
        self.mac_address = data["device_mac_address"] 
        self.project_name = data["project_name"] 
        self.start_time = data["start_time"] 
        self.end_time = data["end_time"] if "end_time" in data else None
    
    def to_template_data_format(self) -> dict:
        template_data = {
            "mac_address": self.mac_address,
            "project_name": self.project_name,
            "start_time": self.start_time,
        }
        if self.github_link:
            template_data["end_time"] = self.end_time

        return template_data


    def is_active(self) -> bool:
        return True if self.end_time else False

    def time_since_start(self) -> datetime.timedelta:
        timestamp_datetime = datetime.strptime(self.start_time, '%Y-%m-%d %H:%M:%S')
        current_time = datetime.now()

        time_dff = current_time - timestamp_datetime
        # print("time difference " + str(time_dff.days))

        # Extract hours, minutes, and seconds from the time difference
        days = time_dff.days
        hours, remainder = divmod(time_dff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

    