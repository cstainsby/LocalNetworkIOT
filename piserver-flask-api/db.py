from flask import g
import sqlite3
from sqlite3 import Connection, Cursor
import os


class PiDatabase():
    def __init__(self, debug_mode=False) -> None:
        print("------------- INITIALIZING DATABASE -------------")
        if debug_mode:
            self.DATABASE_NAME = 'test.db'
            print("Set to debug mode")
        else:
            self.DATABASE_NAME = 'pi_server.db'
            print("Set to production mode")

        self.db_path = os.path.join(os.getcwd(), self.DATABASE_NAME)
        database_exist = os.path.exists(self.db_path)

        print("database " + self.db_path 
            + (" does " if database_exist else " doesn't ") + "exist")

        # if debug_mode and database_exist: os.remove(self.db_path)

        conn = sqlite3.connect(self.DATABASE_NAME)
        cursor = conn.cursor()
        
        if not database_exist:
            print("Creating new database instance...")
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
                print("Loading base production values...")
                with open("sql/insertInitialValues.sql", 'r') as sql_file:
                    file_contents = sql_file.read()
                    cursor.executescript(file_contents)
                conn.commit()
        print("-------------------------------------------------")

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
    
    def add_device_log(self, db_cursor: Cursor):
        db_cursor.execute('''
            INSERT INTO device_log_table (creation_time, mac_address, log_data)
            VALUES (?, ?, ?)
        ''', ())    
    
    def get_device_logs_by_parameters(self, db_cursor: Cursor, 
        device_addr: str = None, 
        date_from: str = None, 
        date_to: str = None,
        checkout_id: int = None,
        status_code: int = None, 
        filter_topics: list= [],
        order_by_topics: list = [],
        order_by_asc_or_desc = "ASC"
    ):
        sql_build_query = '''
            SELECT dev.mac_address, dev.device_name, dev.device_type, 
                log.creation_time, log.status_code, log.log_data,
                checkout.checkout_id, user.fname, user.lname
            FROM device_log_table log
                JOIN registered_device_table dev ON (log.mac_address = dev.mac_address)
                JOIN device_user_checkout_table checkout ON (log.mac_address = checkout.device_mac_address)
                JOIN user_table user ON (checkout.user_id = user.user_id)
            WHERE 1=1
        '''

        # append additional where clauses if necessary
        if device_addr:
            sql_build_query += f" AND dev.mac_address = '{device_addr}'"
        if date_from:
            sql_build_query += f" AND log.creation_time >= '{date_from}'"
        if date_to:
            sql_build_query += f" AND log.creation_time <= '{date_to}'"
        if checkout_id:
            sql_build_query += f" AND checkout.checkout_id = '{checkout_id}'"
        if status_code:
            sql_build_query += f" AND log.status_code = '{status_code}'"
        # if filter_topics and len(filter_topics) > 0:
        #     for topic in filter_topics:
        #         sql_build_query += f" AND log_data LIKE '%\"{topic}\":%'"
        # if order_by_topics:
        #     order_by_clause = ", ".join(order_by_topics)
        #     sql_build_query += f" ORDER BY {order_by_clause} {order_by_asc_or_desc}"
        
        db_cursor.execute(sql_build_query + ';')
        return db_cursor.fetchall()
    
    def get_all_projects(self, db_cursor: Cursor):
        db_cursor.execute('''
            SELECT * 
            FROM project_table
        ''')
        return db_cursor.fetchall()

    def get_project_by_name(self, db_cursor: Cursor, project_name: str):
        db_cursor.execute(f'''
            SELECT * 
            FROM project_table
            WHERE project_name = '{project_name}'
        ''')
        return db_cursor.fetchone()
    
    def get_devices_by_project_name(self, db_cursor: Cursor, project_name: str):
        '''
        Get all devices associated with a project
        '''
        db_cursor.execute(f'''
            SELECT * 
            FROM registered_device_table dev 
                JOIN device_user_checkout_table checkout ON (dev.mac_address = checkout.device_mac_address)
            WHERE project_name = '{project_name}'
        ''')
        return db_cursor.fetchall()

    def add_dog_motion_data(self, db_cursor: Cursor, data):
        db_cursor.execute('''
            INSERT INTO motion_data (accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data.accel_x, data.accel_y, data.accel_z, data.gyro_x, data.gyro_y, data.gyro_z))

    def get_dog_motion_data(self):
        pass
