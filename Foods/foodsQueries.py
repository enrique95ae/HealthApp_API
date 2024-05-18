CREATE_FOODS_TABLE = '''
CREATE TABLE IF NOT EXISTS FOODS (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    PortionSize REAL NOT NULL,
    Calories REAL NOT NULL,
    TotalFat REAL NOT NULL,
    SaturatedFat REAL NOT NULL,
    Sodium REAL NOT NULL,  -- Stored in g
    TotalCarbs REAL NOT NULL,
    DietaryFiber REAL NOT NULL,
    Sugars REAL NOT NULL,
    Proteins REAL NOT NULL,
    Cholesterol REAL NOT NULL,  -- Stored in g
    UNIQUE(Name)
);
'''

SELECT_ALL_FOODS = 'SELECT * FROM FOODS;'

SELECT_FOOD_BY_ID = 'SELECT * FROM FOODS WHERE Id = ?;'

SELECT_FOOD_BY_NAME = 'SELECT * FROM FOODS WHERE Name = ?;'

CHECK_DUPLICATE_FOOD = 'SELECT * FROM FOODS WHERE Name = ?;'

INSERT_FOOD = '''
INSERT INTO FOODS (Name, PortionSize, Calories, TotalFat, SaturatedFat, Sodium, TotalCarbs, DietaryFiber, Sugars, Proteins, Cholesterol)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
'''

UPDATE_FOOD_BY_ID = '''
UPDATE FOODS SET
    Name = ?, PortionSize = ?, Calories = ?, TotalFat = ?, SaturatedFat = ?, 
    Sodium = ?, TotalCarbs = ?, DietaryFiber = ?, Sugars = ?, Proteins = ?, Cholesterol = ?
WHERE Id = ?;
'''

