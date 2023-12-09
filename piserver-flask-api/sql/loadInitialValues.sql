INSERT INTO user_table (fname, lname, identification_num)
SELECT 'Cole', 'Stainsby', 1
WHERE NOT EXISTS (
    SELECT 1 FROM user_table 
    WHERE fname = 'Cole' AND lname = 'Stainsby'
    LIMIT 1
);

INSERT INTO user_table (fname, lname, identification_num)
SELECT 'Ross', 'Stainsby', 2
WHERE NOT EXISTS (
    SELECT 1 FROM user_table 
    WHERE fname = 'Ross' AND lname = 'Stainsby'
    LIMIT 1
);

INSERT INTO user_table (fname, lname, identification_num)
SELECT 'Susan', 'Stainsby', 3
WHERE NOT EXISTS (
    SELECT 1 FROM user_table 
    WHERE fname = 'Susan' AND lname = 'Stainsby'
    LIMIT 1
);

INSERT INTO user_table (fname, lname, user_desc, identification_num)
SELECT 'Scout', 'Stainsby', "dog", 4
WHERE NOT EXISTS (
    SELECT 1 FROM user_table 
    WHERE fname = 'Scout' AND lname = 'Stainsby'
    LIMIT 1
);


INSERT INTO project_table (project_name, project_desc, created_on, github_link)
VALUES 
    ("dogTrackerProject", "A fun IOT project to track my dogs movement", '2023-11-21 10:12:00', "https://github.com/cstainsby/DogTracker"),
    ("piLocalServer", "A home server hosted on my raspberry pi", '2023-11-21 10:12:00', 'https://github.com/cstainsby/PiLocalNetwork');