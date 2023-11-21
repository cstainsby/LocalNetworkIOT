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
    def __init__(self, 
                device_name: str, 
                mac_address: str,
                device_description: str) -> None:
        self.device_name = device_name
        self.mac_address = mac_address
        self.device_description = device_description

        self.start_time

        self.device_checkouts = []

    def is_active() -> bool:
        return False

    def time_since_start() -> datetime.timedelta:
        timestamp_datetime = datetime.strptime(self.start_time, '%Y-%m-%d %H:%M:%S')
        current_time = datetime.now()

        time_dff = current_time - timestamp_datetime
        # print("time difference " + str(time_dff.days))

        # Extract hours, minutes, and seconds from the time difference
        days = time_dff.days
        hours, remainder = divmod(time_dff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)