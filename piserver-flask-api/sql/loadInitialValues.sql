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
