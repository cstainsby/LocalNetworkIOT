
from user import User
from project import Project

class DeviceCheckout():
    def __init__(self, checkout_data) -> None:
        self.checked_out_to = User({
            
        })
        self.checked_device = Project


    def is_active(self) -> bool:
        

        return False

    def time_since_start(self) -> datetime.timedelta:
        timestamp_datetime = datetime.strptime(self.start_time, '%Y-%m-%d %H:%M:%S')
        current_time = datetime.now()

        time_dff = current_time - timestamp_datetime
        # print("time difference " + str(time_dff.days))

        # Extract hours, minutes, and seconds from the time difference
        days = time_dff.days
        hours, remainder = divmod(time_dff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)