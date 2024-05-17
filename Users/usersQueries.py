CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS USERS (
    Id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    DoB TEXT NOT NULL,
    Weight REAL NOT NULL,
    Height REAL NOT NULL,
    BodyType TEXT NOT NULL,
    Goal TEXT NOT NULL,
    Username TEXT NOT NULL UNIQUE,
    Password TEXT NOT NULL
);
"""

SELECT_ALL_USERS = "SELECT * FROM USERS;"
SELECT_USER_BY_ID = "SELECT * FROM USERS WHERE Id = ?;"
SELECT_USER_BY_USERNAME = "SELECT * FROM USERS WHERE Username = ?;"
INSERT_USER = """
INSERT INTO USERS (Name, DoB, Weight, Height, BodyType, Goal, Username, Password)
VALUES (?, ?, ?, ?, ?, ?, ?, ?);
"""
UPDATE_USER_BY_ID = """
UPDATE USERS SET
    Name = ?, DoB = ?, Weight = ?, Height = ?, BodyType = ?, Goal = ?, Username = ?, Password = ?
WHERE Id = ?;
"""
