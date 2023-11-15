from flask import g
import sqlite3
from sqlite3 import Connection, Cursor
import os

from datatypes import MPU6050_Data

class PiDatabase():
    def __init__(self, debug_mode=False) -> None:
        if debug_mode:
            self.DATABASE_NAME = 'test.db'
        else:
            self.DATABASE_NAME = 'pi_server.db'

        self.db_path = os.path.join(os.getcwd(), self.DATABASE_NAME)
        database_exist = os.path.exists(self.db_path)

        conn = sqlite3.connect(self.DATABASE_NAME)
        cursor = conn.cursor()
        
        if not database_exist:
            with open("sql/initDB.sql", 'r') as sql_file:
                file_contents = sql_file.read()
                cursor.executescript(file_contents)
            conn.commit()

            if debug_mode:
                print("Loading Test Data...")
                with open("sql/loadTestValues.sql", 'r') as sql_file:
                    file_contents = sql_file.read()
                    cursor.executescript(file_contents)
                conn.commit()
            else:
                with open("sql/insertInitialValues.sql", 'r') as sql_file:
                    file_contents = sql_file.read()
                    cursor.executescript(file_contents)
                conn.commit()

    def get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(self.DATABASE_NAME)
        return db

    def get_user_by_id(self, db_cursor: Cursor, id: int):
        '''
        get a user by id 
        '''
        db_cursor.execute("""
            SELECT * 
            FROM user_table u
            WHERE u.user_id = ? 
        """, (id,))
        return db_cursor.fetchone()

    def get_all_devices(self, db_cursor: Cursor):
        '''
        Get all devices currently registered to the system
        '''
        db_cursor.execute("""
            SELECT * FROM registered_device_table
        """)
        return db_cursor.fetchall()
    
    def get_deactivated_devices(self, db_cursor: Cursor):
        db_cursor.execute("""
            SELECT dev.mac_address, dev.device_name, dev.device_desc,
                checkout.end_time
            FROM registered_device_table dev 
                JOIN device_user_checkout_table checkout ON (dev.mac_address = checkout.device_mac_address)
            WHERE checkout.end_time IS NOT NULL 
        """)
        return db_cursor.fetchall()

    def get_active_devices_with_user_info(self, db_cursor: Cursor):
        db_cursor.execute("""
            SELECT dev.mac_address, dev.device_name, dev.device_desc, 
                checkout.start_time, 
                user.fname, user.lname 
            FROM registered_device_table dev 
                JOIN device_user_checkout_table checkout ON (dev.mac_address = checkout.device_mac_address)
                JOIN user_table user ON (user.user_id = checkout.user_id)
            WHERE checkout.end_time IS NULL 
        """)
        return db_cursor.fetchall()

    def add_dog_motion_data(self, db_cursor: Cursor, data: MPU6050_Data):
        db_cursor.execute('''
            INSERT INTO motion_data (accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data.accel_x, data.accel_y, data.accel_z, data.gyro_x, data.gyro_y, data.gyro_z))

    def get_dog_motion_data(self):
        pass
