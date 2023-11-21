
-- Inserting data into registered_device_table
INSERT INTO registered_device_table (mac_address, device_name, device_type, device_desc) VALUES 
    ('00:11:22:33:44:55', 'Device1', 'MPU6050', 'Description for Device1'),
    ('AA:BB:CC:DD:EE:FF', 'Device2', 'MPU6050', 'Description for Device2'),
    ('11:22:33:44:55:66', 'Device3', 'MPU6050', 'Description for Device3'),
    ('22:33:44:55:66:77', 'Device4', 'RaspberryPi', 'Description for Device4'),
    ('33:44:55:66:77:88', 'Device5', 'MPU6050', 'Description for Device5'),
    ('44:55:66:77:88:99', 'Device6', 'RaspberryPi', 'Description for Device6');


-- Inserting data into device_user_checkout_table
INSERT INTO device_user_checkout_table (device_mac_address, user_id, project_id, start_time, end_time) VALUES 
    ('00:11:22:33:44:55', 1, 1, '2023-01-01 12:00:00', '2023-01-01 14:00:00'),
    ('AA:BB:CC:DD:EE:FF', 2, NULL, '2023-01-02 09:30:00', '2023-01-02 11:45:00'),
    ('11:22:33:44:55:66', 3, NULL, '2023-01-03 15:45:00', NULL),
    ('22:33:44:55:66:77', 1, 1, '2023-01-04 08:00:00', NULL),
    ('33:44:55:66:77:88', 2, NULL, '2023-01-05 12:30:00', '2023-01-05 14:45:00'),
    ('44:55:66:77:88:99', 2, NULL, '2023-01-06 16:45:00', NULL);

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


INSERT INTO user_table (fname, lname, user_desc)
SELECT 'John', 'Doe', 'Software Developer'
WHERE NOT EXISTS (
    SELECT 1 FROM user_table 
    WHERE fname = 'John' AND lname = 'Doe'
    LIMIT 1
);

INSERT INTO user_table (fname, lname, user_desc)
SELECT 'Jane', 'Smith', 'Data Analyst'
WHERE NOT EXISTS (
    SELECT 1 FROM user_table 
    WHERE fname = 'Jane' AND lname = 'Smith'
    LIMIT 1
);

INSERT INTO user_table (fname, lname, user_desc)
SELECT 'Alice', 'Johnson', 'Database Administrator'
WHERE NOT EXISTS (
    SELECT 1 FROM user_table 
    WHERE fname = 'Alice' AND lname = 'Johnson'
    LIMIT 1
);

INSERT INTO user_table (fname, lname, user_desc)
SELECT 'Bob', 'Williams', 'Network Engineer'
WHERE NOT EXISTS (
    SELECT 1 FROM user_table 
    WHERE fname = 'Bob' AND lname = 'Williams'
    LIMIT 1
);

INSERT INTO device_log_table (creation_time, status_code, mac_address, log_data)
VALUES
    ('2023-01-01 12:00:00', 0, '00:11:22:33:44:55', '{"entry_number": 1, "random_value": 0.123}'),
    ('2023-01-02 12:30:00', 1, 'AA:BB:CC:DD:EE:FF', '{"entry_number": 2, "random_value": 0.456}'),
    ('2023-01-03 13:00:00', 2, '11:22:33:44:55:66', '{"entry_number": 3, "random_value": 0.789}'),
    ('2023-01-04 13:30:00', 1, '22:33:44:55:66:77', '{"entry_number": 4, "random_value": 0.234}'),
    ('2023-01-05 14:00:00', 0, '33:44:55:66:77:88', '{"entry_number": 5, "random_value": 0.567}'),
    ('2023-01-06 14:30:00', 0, '44:55:66:77:88:99', '{"entry_number": 6, "random_value": 0.890}'),
    ('2023-01-07 15:00:00', 1, '00:11:22:33:44:55', '{"entry_number": 7, "random_value": 0.123}'),
    ('2023-01-08 15:30:00', 1, 'AA:BB:CC:DD:EE:FF', '{"entry_number": 8, "random_value": 0.456}'),
    ('2023-01-09 16:00:00', 2, '11:22:33:44:55:66', '{"entry_number": 9, "random_value": 0.789}'),
    ('2023-01-10 16:30:00', 2, '22:33:44:55:66:77', '{"entry_number": 10, "random_value": 0.234}'),
    ('2023-01-11 17:00:00', 0, '33:44:55:66:77:88', '{"entry_number": 11, "random_value": 0.567}'),
    ('2023-01-12 17:30:00', 1, '44:55:66:77:88:99', '{"entry_number": 12, "random_value": 0.890}'),
    ('2023-01-13 18:00:00', 2, '00:11:22:33:44:55', '{"entry_number": 13, "random_value": 0.123}'),
    ('2023-01-14 18:30:00', 0, 'AA:BB:CC:DD:EE:FF', '{"entry_number": 14, "random_value": 0.456}'),
    ('2023-01-15 19:00:00', 0, '11:22:33:44:55:66', '{"entry_number": 15, "random_value": 0.789}'),
    ('2023-01-16 19:30:00', 0, '22:33:44:55:66:77', '{"entry_number": 16, "random_value": 0.234}');

INSERT INTO project_table (project_name, project_desc, created_on, github_link)
VALUES 
    ("Dog Tracker Project", "A fun IOT project to track my dogs movement", '2023-11-21 10:12:00', "https://github.com/cstainsby/DogTracker"),
    ("Pi Local Server", "A home server hosted on my raspberry pi", '2023-11-21 10:12:00', 'https://github.com/cstainsby/PiLocalNetwork');