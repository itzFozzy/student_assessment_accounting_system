DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS UserRole;
DROP TABLE IF EXISTS GroupList;
DROP TABLE IF EXISTS DisciplineList;
DROP TABLE IF EXISTS MarkList;

CREATE TABLE UserRole (
    userRoleID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE GroupList (
    groupID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE DisciplineList (
    disciplineID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE Users (
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    patronymik TEXT,
    login TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    userRole INTEGER NOT NULL,
    group INTEGER NOT NULL,

    FOREIGN KEY (userRole) REFERENCES UserRole (userRoleID),
    FOREIGN KEY (group) REFERENCES GroupList (groupID)
);

CREATE TABLE MarkList (
    markID INTEGER PRIMARY KEY AUTOINCREMENT,
    mark INTEGER NOT NULL,
    avgmark FLOAT NOT NULL,
    studentID INTEGER NOT NULL,
    prepodID INTEGER NOT NULL,
    disciplineID INTEGER NOT NULL,

    FOREIGN KEY (studentID) REFERENCES Users (userID),
    FOREIGN KEY (prepodID) REFERENCES Users (userID) ,
    FOREIGN KEY (disciplineID) REFERENCES DisciplineList (disciplineID)
);

INSERT INTO UserRole(name)
VALUES ('Student'), ('Prepod'), ('Admin');
