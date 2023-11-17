

-- --------------------------------------------------------------------------------
--                                 ACTIVE TABLES 
-- --------------------------------------------------------------------------------
--   registered_device_table 
--       Used to store meta-information regarding devices used in combonation with
--       this specific api setup
--
--   user_table
--       users which can use the devices, note that this can include non-human 
--       entities  
--
--   device_user_checkout_table
--       Know who has a specific device based on a checkout system
--   
--   mpu6050_data_table
--       data generated from an mpu6050
-- --------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS registered_device_table (
    mac_address TEXT PRIMARY KEY,
    device_name TEXT NOT NULL,
    device_type TEXT NOT NULL,
    device_desc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS user_table (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fname TEXT NOT NULL,
    lname TEXT NOT NULL,
    user_desc TEXT,
    identification_num INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS device_user_checkout_table (
    checkout_id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_mac_address TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT, 
    FOREIGN KEY (device_mac_address) REFERENCES registered_device_table(mac_address),
    FOREIGN KEY (user_id) REFERENCES user_table(user_id)
);

CREATE TABLE IF NOT EXISTS mpu6050_data_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    creation_time TEXT NOT NULL, -- date
    generated_by TEXT NOT NULL, -- mac address of device that generated the data
    accel_x REAL NOT NULL,
    accel_y REAL NOT NULL,
    accel_z REAL NOT NULL,
    gyro_x REAL NOT NULL,
    gyro_y REAL NOT NULL,
    gyro_z REAL NOT NULL,
    FOREIGN KEY (generated_by) REFERENCES registered_device_table(mac_address)
);



CREATE TABLE IF NOT EXISTS device_log_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    creation_time TEXT NOT NULL, 
    -- device_type TEXT NOT NULL, 
    -- status_code INTEGER NOT NULL,
    mac_address TEXT NOT NULL, -- device that made the log
    log_data TEXT NOT NULL, -- json formatted log data
    FOREIGN KEY (mac_address) REFERENCES registered_device_table(mac_address)
);