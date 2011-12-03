-- SQL for creating our SQLite table(s)

-- Tried to add CHECK constraints, but they don't seem to work in sqlite :(
CREATE TABLE ClimateGrid (
    Row INT NOT NULL,
    Col INT NOT NULL,
    Precip FLOAT,
    Min_T FLOAT,
    Max_T FLOAT,
    Seq INT NOT NULL,
    Year INT NOT NULL,
    Month INT NOT NULL,
    Day INT NOT NULL);
--CHECK (Row > 0 AND Row < 720)
--CHECK (Col > 0 AND Col < 360)
--CHECK (Year > 0)

-- Create indices
CREATE INDEX GridIndex ON ClimateGrid (Row, Col);
CREATE INDEX DateIndex ON ClimateGrid (Year, Month, Day);

-- Create test data
INSERT INTO ClimateGrid (Row, Col, Precip, Min_T, Max_T, Seq, Year, Month, Day)
    VALUES (180, 180, 3.0, -5, 100, 180 * 720 + 180, 1998, 3, 5);

-- Insert Data template
--INSERT INTO ClimateGrid (Row, Col, Precip, Min_T, Max_T, Seq, Year, Month, Day)
    --VALUES ();
