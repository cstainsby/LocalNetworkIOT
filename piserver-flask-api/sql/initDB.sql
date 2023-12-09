

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
    device_desc TEXT NOT NULL,
    github_link TEXT
);

CREATE TABLE IF NOT EXISTS project_table (
    project_name TEXT PRIMARY KEY,
    project_desc TEXT NOT NULL,
    created_on TEXT NOT NULL,
    github_link TEXT
);


CREATE TABLE IF NOT EXISTS device_recording_table (
    recording_id INTEGER PRIMARY KEY AUTOINCREMENT,
    recording_name TEXT NOT NULL,
    device_checked_out INTEGER NOT NULL,  -- allows a recording to be associated with a 
    user_id INTEGER NOT NULL, -- user who made this recording
    start_time TEXT NOT NULL,
    end_time TEXT,
    FOREIGN KEY (device_checked_out) REFERENCES device_user_checkout_table(checkout_id)
);

-- records all recordings made under a project
CREATE TABLE IF NOT EXISTS project_recording_table (
    project_recording_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT NOT NULL,
    recording_id INTEGER NOT NULL,
    FOREIGN KEY (project_name) REFERENCES project_table(project_name),
    FOREIGN KEY (recording_id) REFERENCES recording_table(recording_id)
);

CREATE TABLE IF NOT EXISTS user_table (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fname TEXT NOT NULL,
    lname TEXT NOT NULL,
    user_desc TEXT
);

-- CREATE TABLE IF NOT EXISTS device_user_checkout_table (
--     checkout_id INTEGER PRIMARY KEY AUTOINCREMENT,
--     device_mac_address TEXT NOT NULL,
--     project_name TEXT, -- allow a device to be optionally checked out under a specific project
--     user_id INTEGER NOT NULL,
--     start_time TEXT NOT NULL,
--     end_time TEXT, 
--     FOREIGN KEY (device_mac_address) REFERENCES registered_device_table(mac_address),
--     FOREIGN KEY (user_id) REFERENCES user_table(user_id),
--     FOREIGN KEY (project_name) REFERENCES project_table(project_name)
-- );

CREATE TABLE IF NOT EXISTS device_log_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    creation_time TEXT NOT NULL, 
    status_code INTEGER NOT NULL, -- either 0, 1, or 2 for respectivley informational, error, and success
    mac_address TEXT NOT NULL, -- device that made the log
    log_data TEXT NOT NULL, -- json formatted log data
    FOREIGN KEY (mac_address) REFERENCES registered_device_table(mac_address)
);


-- -----------------------------------------------------------------
--  Data tables
--  These tables should all define how data should be stored for 
--  different inputs. Each should reference a specific recording
--  in the recording table.
-- -----------------------------------------------------------------
CREATE TABLE IF NOT EXISTS mpu6050_data_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recording_id INTEGER NOT NULL, -- the recording which you are generating for
    creation_time TEXT NOT NULL, -- date
    generated_by TEXT NOT NULL, -- mac address of device that generated the data
    accel_x REAL NOT NULL,
    accel_y REAL NOT NULL,
    accel_z REAL NOT NULL,
    gyro_x REAL NOT NULL,
    gyro_y REAL NOT NULL,
    gyro_z REAL NOT NULL,
    FOREIGN KEY (generated_by) REFERENCES registered_device_table(mac_address),
    FOREIGN KEY (recording_id) REFERENCES recording_table(recording_id)
);
