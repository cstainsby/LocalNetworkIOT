
class MPU6050_Data:
    def __init__(self) -> None:
        self.accel_x: float = None
        self.accel_y: float = None
        self.accel_z: float = None
        self.gyro_x: float = None
        self.gyro_y: float = None
        self.gyro_z: float = None
    
    def __init__(self, json) -> None:
        self.accel_x: float = json.accel_x if json.accel_x else None  
        self.accel_y: float = json["accel_y"] if json["accel_y"] else None 
        self.accel_z: float = json["accel_z"] if json["accel_z"] else None 
        self.gyro_x: float = json["gyro_x"] if json["gyro_x"] else None 
        self.gyro_y: float = json["gyro_y"] if json["gyro_y"] else None 
        self.gyro_z: float = json["gyro_z"] if json["gyro_z"] else None 

    def __str__(self) -> str:
        return """
            {
                accel_x: {accel_x},\n
                accel_y: {accel_y},\n
                accel_z: {accel_z},\n
                gyro_x: {gyro_x},\n
                gyro_y: {gyro_y},\n
                gyro_z: {gyro_z}\n
            }""".format(
                accel_x=self.accel_x,
                accel_y=self.accel_y,
                accel_z=self.accel_z,
                gyro_x=self.gyro_x,
                gyro_y=self.gyro_y,
                gyro_z=self.gyro_z
            )

