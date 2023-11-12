import sqlite3

from datatypes import MPU6050_Data

class PiDatabase():
    def __init__(self) -> None:
        self.DATABASE_NAME = 'pi_server.db'
        self.conn = sqlite3.connect(self.DATABASE_NAME)
        self.cursor = self.conn.cursor()

        # Create a table to store motion data if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS motion_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                accel_x REAL,
                accel_y REAL,
                accel_z REAL,
                gyro_x REAL,
                gyro_y REAL,
                gyro_z REAL
            )
        ''')
        self.conn.commit()


    def add_dog_motion_data(self, data: MPU6050_Data):
        self.cursor.execute('''
            INSERT INTO motion_data (accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data.accel_x, data.accel_y, data.accel_z, data.gyro_x, data.gyro_y, data.gyro_z))
        self.conn.commit()
