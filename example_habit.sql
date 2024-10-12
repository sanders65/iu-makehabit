/*
This file contains example data for habits and tracking.
With this, it is possible to test the functionality of "Make it a Habit".
*/

-- First: Create the table 'habits' if it doesn't exists
CREATE TABLE IF NOT EXISTS habits(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    periodicity TEXT,
    creation_date DATE
);

-- Second: Create the table 'tracking' if it doesn't exists
CREATE TABLE IF NOT EXISTS tracking(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id INTEGER,
    checkoff_date DATE,
    FOREIGN KEY (habit_id) REFERENCES habits(id)
);

-- Third: Insert example habit data

-- two daily habits
INSERT INTO habits (name, description, periodicity, creation_date) 
VALUES ('Go for a walk', 'Get some air', 'daily', '2024-09-09 00:00:00');

INSERT INTO habits (name, description, periodicity, creation_date) 
VALUES ('Do exercises', 'Strengthen your body', 'daily', '2024-09-09 00:00:00');

-- three weekly habits
INSERT INTO habits (name, description, periodicity, creation_date) 
VALUES ('Do yoga', 'Connect to your inner self', 'weekly', '2024-08-28 00:00:00');

INSERT INTO habits (name, description, periodicity, creation_date) 
VALUES ('Visit a friend', 'Care for your social skills', 'weekly', '2024-09-03 00:00:00');

INSERT INTO habits (name, description, periodicity, creation_date) 
VALUES ('Read the newspaper', 'Keep being informed', 'weekly', '2024-09-01 00:00:00');

-- Fourth: Insert example tracking data

-- Habit 1: daily, Go for a walk, with breaks, longest streak = 12 days
INSERT INTO tracking (habit_id, checkoff_date) VALUES (1, '2024-09-09 00:00:00'); -- streak 1 (starting week 1)
INSERT INTO tracking (habit_id, checkoff_date) VALUES (1, '2024-09-10 00:00:00'); -- streak 2
INSERT INTO tracking (habit_id, checkoff_date) VALUES (1, '2024-09-11 00:00:00'); -- streak 3
INSERT INTO tracking (habit_id, checkoff_date) VALUES (1, '2024-09-12 00:00:00'); -- streak 4
INSERT INTO tracking (habit_id, checkoff_date) VALUES (1, '2024-09-13 00:00:00'); -- streak 5
INSERT INTO tracking (habit_id, checkoff_date) VALUES (1, '2024-09-14 00:00:00'); -- streak 6
INSERT INTO tracking (habit_id, checkoff_date) VALUES (1, '2024-09-15 00:00:00'); -- streak 7
INSERT INTO tracking (habit_id, checkoff_date) VALUES (1, '2024-09-16 00:00:00'); -- streak 8 (starting week 2)
INSERT INTO tracking (habit_id, checkoff_date) VALUES (1, '2024-09-17 00:00:00'); -- streak 9
INSERT INTO tracking (habit_id, checkoff_date) VALUES (1, '2024-09-20 00:00:00'); -- streak 1 after break 1
INSERT INTO tracking (habit_id, checkoff_date) VALUES (1, '2024-09-21 00:00:00'); -- streak 2
INSERT INTO tracking (habit_id, checkoff_date) VALUES (1, '2024-09-22 00:00:00'); -- streak 3
INSERT INTO tracking (habit_id, checkoff_date) VALUES (1, '2024-09-23 00:00:00'); -- streak 4 (starting week 3)
INSERT INTO tracking (habit_id, checkoff_date) VALUES (1, '2024-09-25 00:00:00'); -- streak 1 after break 2
INSERT INTO tracking (habit_id, checkoff_date) VALUES (1, '2024-09-26 00:00:00'); -- streak 2
INSERT INTO tracking (habit_id, checkoff_date) VALUES (1, '2024-09-27 00:00:00'); -- streak 3
INSERT INTO tracking (habit_id, checkoff_date) VALUES (1, '2024-09-28 00:00:00'); -- streak 4
INSERT INTO tracking (habit_id, checkoff_date) VALUES (1, '2024-09-29 00:00:00'); -- streak 5
INSERT INTO tracking (habit_id, checkoff_date) VALUES (1, '2024-09-30 00:00:00'); -- streak 6 (starting week 4)
INSERT INTO tracking (habit_id, checkoff_date) VALUES (1, '2024-10-01 00:00:00'); -- streak 7
INSERT INTO tracking (habit_id, checkoff_date) VALUES (1, '2024-10-02 00:00:00'); -- streak 8
INSERT INTO tracking (habit_id, checkoff_date) VALUES (1, '2024-10-03 00:00:00'); -- streak 9
INSERT INTO tracking (habit_id, checkoff_date) VALUES (1, '2024-10-04 00:00:00'); -- streak 10
INSERT INTO tracking (habit_id, checkoff_date) VALUES (1, '2024-10-05 00:00:00'); -- streak 11
INSERT INTO tracking (habit_id, checkoff_date) VALUES (1, '2024-10-06 00:00:00'); -- streak 12

-- Habit 2: daily, Do exercises, no breaks, longest streak = 28 days
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-09-09 00:00:00'); -- streak 1 (starting week 1)
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-09-10 00:00:00'); -- streak 2
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-09-11 00:00:00'); -- streak 3
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-09-12 00:00:00'); -- streak 4
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-09-13 00:00:00'); -- streak 5
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-09-14 00:00:00'); -- streak 6
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-09-15 00:00:00'); -- streak 7
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-09-16 00:00:00'); -- streak 8 (starting week 2)
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-09-17 00:00:00'); -- streak 9
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-09-18 00:00:00'); -- streak 10
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-09-19 00:00:00'); -- streak 11
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-09-20 00:00:00'); -- streak 12
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-09-21 00:00:00'); -- streak 13
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-09-22 00:00:00'); -- streak 14
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-09-23 00:00:00'); -- streak 15 (starting week 3)
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-09-24 00:00:00'); -- streak 16
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-09-25 00:00:00'); -- streak 17
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-09-26 00:00:00'); -- streak 18
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-09-27 00:00:00'); -- streak 19
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-09-28 00:00:00'); -- streak 20
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-09-29 00:00:00'); -- streak 21
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-09-30 00:00:00'); -- streak 22 (starting week 4)
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-10-01 00:00:00'); -- streak 23
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-10-02 00:00:00'); -- streak 24
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-10-03 00:00:00'); -- streak 25
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-10-04 00:00:00'); -- streak 26
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-10-05 00:00:00'); -- streak 27
INSERT INTO tracking (habit_id, checkoff_date) VALUES (2, '2024-10-06 00:00:00'); -- streak 28

-- Habit 3: weekly, Do yoga, with break, longest streak = 2 weeks
INSERT INTO tracking (habit_id, checkoff_date) VALUES (3, '2024-08-28 00:00:00'); -- streak 1 
INSERT INTO tracking (habit_id, checkoff_date) VALUES (3, '2024-09-05 00:00:00'); -- streak 2
INSERT INTO tracking (habit_id, checkoff_date) VALUES (3, '2024-09-17 00:00:00'); -- streak 1
INSERT INTO tracking (habit_id, checkoff_date) VALUES (3, '2024-09-26 00:00:00'); -- streak 2

-- Habit 4: weekly, Visit a friend, no break, longest streak = 4 weeks
INSERT INTO tracking (habit_id, checkoff_date) VALUES (4, '2024-09-03 00:00:00'); -- streak 1 
INSERT INTO tracking (habit_id, checkoff_date) VALUES (4, '2024-09-12 00:00:00'); -- streak 2
INSERT INTO tracking (habit_id, checkoff_date) VALUES (4, '2024-09-17 00:00:00'); -- streak 3
INSERT INTO tracking (habit_id, checkoff_date) VALUES (4, '2024-09-27 00:00:00'); -- streak 4

-- Habit 5: weekly, Read the newspaper, with breaks, longest streak = 1 week
INSERT INTO tracking (habit_id, checkoff_date) VALUES (5, '2024-09-01 00:00:00'); -- streak 1 
INSERT INTO tracking (habit_id, checkoff_date) VALUES (5, '2024-09-09 00:00:00'); -- streak 1
INSERT INTO tracking (habit_id, checkoff_date) VALUES (5, '2024-09-26 00:00:00'); -- streak 1
INSERT INTO tracking (habit_id, checkoff_date) VALUES (5, '2024-10-08 00:00:00'); -- streak 1