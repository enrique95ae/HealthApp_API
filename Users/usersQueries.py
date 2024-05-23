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
# Existing queries...

# Add new queries for weights
CREATE_USER_WEIGHT_TABLE = """
CREATE TABLE IF NOT EXISTS USER_WEIGHT (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    USER_Id INTEGER NOT NULL,
    EntryDate TEXT NOT NULL,
    Weight REAL NOT NULL,
    FOREIGN KEY (USER_Id) REFERENCES USERS(Id) ON DELETE CASCADE,
    UNIQUE(USER_Id, EntryDate)
);
"""

INSERT_USER_WEIGHT = """
INSERT INTO USER_WEIGHT (USER_Id, EntryDate, Weight) VALUES (?, ?, ?)
ON CONFLICT(USER_Id, EntryDate) DO UPDATE SET Weight=excluded.Weight;
"""

SELECT_USER_WEIGHTS = """
SELECT Id, USER_Id, EntryDate, Weight FROM USER_WEIGHT WHERE USER_Id = ? ORDER BY EntryDate DESC;
"""

CHECK_TODAYS_WEIGHT_ENTRY = """
SELECT COUNT(*) FROM USER_WEIGHT
WHERE USER_Id = ? AND EntryDate = ?;
"""
