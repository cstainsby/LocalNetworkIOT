

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
    device_name TEXT,
    device_desc TEXT
);

CREATE TABLE IF NOT EXISTS user_table (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fname TEXT NOT NULL,
    lname TEXT NOT NULL,
    user_desc TEXT,
    identification_num INTEGER NOT NULL
);
-- INSERT OR IGNORE INTO user_table (fname, lname, idetification_num) VALUES ("Cole", "Stainsby", 0)
--     SELECT "Cole", "Stainsby"
--     WHERE NOT EXISTS (SELECT 1 FROM user_table LIMIT 1);
-- INSERT OR IGNORE INTO user_table (fname, lname, idetification_num) VALUES ("Ross", "Stainsby", 1)
--     SELECT "Ross", "Stainsby"
--     WHERE NOT EXISTS (SELECT 1 FROM user_table LIMIT 1);
-- INSERT INTO user_table (fname, lname, idetification_num) VALUES ("Susan", "Stainsby", 2)
-- SELECT "Susan", "Stainsby"
-- WHERE NOT EXISTS (SELECT 1 FROM user_table WHERE fname = "Susan" AND lname = "Stainsby" LIMIT 1);
-- INSERT INTO user_table (fname, lname, user_desc, idetification_num) VALUES ("Scout", "Stainsby", "Dog", 3)
--     SELECT "Scout", "Stainsby", "Dog"
--     WHERE NOT EXISTS (SELECT 1 FROM user_table LIMIT 1);


-- Insert initial values into user_table if users with the same first and last name do not exist


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
    generated_by TEXT NOT NULL,
    accel_x REAL NOT NULL,
    accel_y REAL NOT NULL,
    accel_z REAL NOT NULL,
    gyro_x REAL NOT NULL,
    gyro_y REAL NOT NULL,
    gyro_z REAL NOT NULL,
    FOREIGN KEY (generated_by) REFERENCES registered_device_table(mac_address)
);