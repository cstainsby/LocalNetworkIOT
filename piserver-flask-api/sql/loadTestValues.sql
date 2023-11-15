
-- Inserting data into registered_device_table
INSERT INTO registered_device_table (mac_address, device_name, device_desc) VALUES 
    ('00:11:22:33:44:55', 'Device1', 'Description for Device1'),
    ('AA:BB:CC:DD:EE:FF', 'Device2', 'Description for Device2'),
    ('11:22:33:44:55:66', 'Device3', 'Description for Device3'),
    ('22:33:44:55:66:77', 'Device4', 'Description for Device4'),
    ('33:44:55:66:77:88', 'Device5', 'Description for Device5'),
    ('44:55:66:77:88:99', 'Device6', 'Description for Device6');


-- Inserting data into device_user_checkout_table
INSERT INTO device_user_checkout_table (device_mac_address, user_id, start_time, end_time) VALUES 
    ('00:11:22:33:44:55', 1, '2023-01-01 12:00:00', '2023-01-01 14:00:00'),
    ('AA:BB:CC:DD:EE:FF', 2, '2023-01-02 09:30:00', '2023-01-02 11:45:00'),
    ('11:22:33:44:55:66', 3, '2023-01-03 15:45:00', NULL),
    ('22:33:44:55:66:77', 1, '2023-01-04 08:00:00', '2023-01-04 10:00:00'),
    ('33:44:55:66:77:88', 2, '2023-01-05 12:30:00', '2023-01-05 14:45:00'),
    ('44:55:66:77:88:99', 2, '2023-01-06 16:45:00', NULL);

-- Inserting data into mpu6050_data_table
INSERT INTO mpu6050_data_table (creation_time, generated_by, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z) VALUES 
    ('2023-01-01 08:00:00', '00:11:22:33:44:55', 0.5, -1.2, 2.0, 0.1, -0.8, 0.5),
    ('2023-01-01 09:15:00', 'AA:BB:CC:DD:EE:FF', 1.2, 0.8, -0.3, -0.2, 0.7, -0.4),
    ('2023-01-01 10:30:00', '11:22:33:44:55:66', -0.3, 0.5, 1.8, 1.0, -1.5, 0.9),
    ('2023-01-02 08:30:00', '00:11:22:33:44:55', 0.8, -1.5, 2.5, -0.3, -0.9, 0.7),
    ('2023-01-02 09:45:00', 'AA:BB:CC:DD:EE:FF', 1.5, 0.3, -0.8, -0.5, 0.6, -0.1),
    ('2023-01-03 12:45:00', '11:22:33:44:55:66', -1.0, 0.8, 1.2, 0.9, -1.2, 1.1),
    ('2023-01-03 14:00:00', 'A1:B2:C3:D4:E5:F6', 0.3, -0.6, 1.5, -0.2, 1.1, -0.7),
    ('2023-01-03 15:30:00', 'C3:D4:E5:F6:A1:B2', -0.5, 1.2, -0.9, 0.8, -0.4, 1.3),
    ('2023-01-04 09:00:00', 'E5:F6:A1:B2:C3:D4', 1.2, 0.7, -0.4, -1.0, 0.6, -0.2),
    ('2023-01-04 10:15:00', 'A1:B2:C3:D4:E5:F6', -0.7, 1.5, 0.2, 0.5, -1.3, 0.9),
    ('2023-01-05 11:30:00', 'C3:D4:E5:F6:A1:B2', 0.9, -0.4, 1.1, 0.3, 0.8, -1.0),
    ('2023-01-05 13:00:00', 'E5:F6:A1:B2:C3:D4', -1.5, 0.2, -1.2, 1.2, -0.7, 0.4);


INSERT INTO user_table (fname, lname, user_desc, identification_num)
SELECT 'John', 'Doe', 'Software Developer', 1
WHERE NOT EXISTS (
    SELECT 1 FROM user_table 
    WHERE fname = 'John' AND lname = 'Doe'
    LIMIT 1
);

INSERT INTO user_table (fname, lname, user_desc, identification_num)
SELECT 'Jane', 'Smith', 'Data Analyst', 2
WHERE NOT EXISTS (
    SELECT 1 FROM user_table 
    WHERE fname = 'Jane' AND lname = 'Smith'
    LIMIT 1
);

INSERT INTO user_table (fname, lname, user_desc, identification_num)
SELECT 'Alice', 'Johnson', 'Database Administrator', 3
WHERE NOT EXISTS (
    SELECT 1 FROM user_table 
    WHERE fname = 'Alice' AND lname = 'Johnson'
    LIMIT 1
);

INSERT INTO user_table (fname, lname, user_desc, identification_num)
SELECT 'Bob', 'Williams', 'Network Engineer', 4
WHERE NOT EXISTS (
    SELECT 1 FROM user_table 
    WHERE fname = 'Bob' AND lname = 'Williams'
    LIMIT 1
);


