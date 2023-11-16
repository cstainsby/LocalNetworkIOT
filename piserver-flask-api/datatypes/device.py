
class Device():
    def __init__(self, 
                device_name: str, 
                mac_address: str,
                device_description: str) -> None:
        self.device_name = device_name
        self.mac_address = mac_address
        self.device_description = device_description