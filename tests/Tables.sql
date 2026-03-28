# Database Pragma
Grades:             : Student Grade
    ID              : Auto Increment ID positional
    Name            : Student Full Name
    Subject         : Subject Taking
    Advisor         : Name of subject Teacher
    GradeLevel      : Current Grade taking (kinder - 6)
    SchoolYear      : Current School Year ex(2026-2027)
    Section         : Section Name
    Grade           : Aquired Gared in Subject

Students:           : Srudent Details
    ID              : Auto Increment ID positional
    Name            : Student Full Name
    Guardian        : Student Gardian (Full Name)
    SchoolYear      : Current School Year ex(2026-2027)
    GradeLevel      : Current Grade taking (kinder - 6)

Subject:            : Subject Details
    ID              : Auto Increment ID positiona
    Subject         : Subject Name
    Advisor         : Name of subject Teacher
    GradeLevel      : Current Grade taking (kinder - 6)

GradeLevel:
    ID              : Auto Increment ID positiona
    GradeLevel      : LevelName (kinder-6)
    Section         : section name
    Advisor         : Name of subject Teacher

Tables
  PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS Levels (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        LevelName TEXT NOT NULL UNIQUE,
        Category TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Sections (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        SectionName TEXT NOT NULL,
        LevelID INTEGER NOT NULL,
        FOREIGN KEY(LevelID) REFERENCES Levels(ID) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS Students (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Guardian TEXT NOT NULL,
        LevelID INTEGER NOT NULL,
        SectionID INTEGER NOT NULL,
        SchoolYear TEXT NOT NULL,
        FOREIGN KEY(LevelID) REFERENCES Levels(ID),
        FOREIGN KEY(SectionID) REFERENCES Sections(ID)
    );

    CREATE TABLE IF NOT EXISTS Subjects (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Subject TEXT NOT NULL,
        Advisor TEXT NOT NULL,
        LevelID INTEGER NOT NULL,
        FOREIGN KEY(LevelID) REFERENCES Levels(ID)
    );

    CREATE TABLE IF NOT EXISTS Grades (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        StudentID INTEGER NOT NULL,
        SubjectID INTEGER NOT NULL,
        Grade TEXT NOT NULL,
        SchoolYear TEXT NOT NULL,
        FOREIGN KEY(StudentID) REFERENCES Students(ID) ON DELETE CASCADE,
        FOREIGN KEY(SubjectID) REFERENCES Subjects(ID) ON DELETE CASCADE
    );