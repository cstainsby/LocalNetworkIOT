import sqlite3
import os

from datatypes import MPU6050_Data

class PiDatabase():
    def __init__(self) -> None:
        self.DATABASE_NAME = 'pi_server.db'

        db_path = os.path.join(os.getcwd(), self.DATABASE_NAME)
        database_exist = os.path.exists(db_path)

        self.conn = sqlite3.connect(self.DATABASE_NAME)
        self.cursor = self.conn.cursor()
        
        if not database_exist:
            with open("sql/initDB.sql", 'r') as sql_file:
                file_contents = sql_file.read()
                self.cursor.executescript(file_contents)
            self.conn.commit()

            with open("sql/insertInitialValues.sql", 'r') as sql_file:
                file_contents = sql_file.read()
                self.cursor.executescript(file_contents)
            self.conn.commit()

    def get_user_by_id(self, id: int):
        '''
        get a user by id 
        '''
        self.cursor.execute("""
            SELECT * 
            FROM user_table u
            WHERE u.user_id = ? 
        """, (id,))
        return self.cursor.fetchone()

    def get_registered_devices(self):
        self.cursor.execute("""
            SELECT 
        """)

    def add_dog_motion_data(self, data: MPU6050_Data):
        self.cursor.execute('''
            INSERT INTO motion_data (accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data.accel_x, data.accel_y, data.accel_z, data.gyro_x, data.gyro_y, data.gyro_z))
        self.conn.commit()
    
    def get_dog_motion_data():
        pass
