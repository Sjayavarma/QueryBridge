import sqlite3
import random
from faker import Faker
from datetime import datetime, timedelta

faker = Faker()

conn = sqlite3.connect("company.db")
cursor = conn.cursor()

# --- Core Tables ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS DEPARTMENT (
    DEPT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    DEPT_NAME TEXT,
    MANAGER_NAME TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS EMPLOYEE (
    EMP_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME TEXT,
    AGE INTEGER,
    GENDER TEXT,
    POSITION TEXT,
    SALARY REAL,
    DEPT_ID INTEGER,
    EMAIL TEXT,
    FOREIGN KEY (DEPT_ID) REFERENCES DEPARTMENT(DEPT_ID)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS PROJECT (
    PROJECT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    PROJECT_NAME TEXT,
    START_DATE TEXT,
    END_DATE TEXT,
    BUDGET REAL,
    DEPT_ID INTEGER,
    FOREIGN KEY (DEPT_ID) REFERENCES DEPARTMENT(DEPT_ID)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS ASSIGNMENT (
    ASSIGNMENT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    EMP_ID INTEGER,
    PROJECT_ID INTEGER,
    ROLE TEXT,
    HOURS_PER_WEEK INTEGER,
    FOREIGN KEY (EMP_ID) REFERENCES EMPLOYEE(EMP_ID),
    FOREIGN KEY (PROJECT_ID) REFERENCES PROJECT(PROJECT_ID)
);
""")

# --- Extended Tables ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS SKILL (
    SKILL_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    SKILL_NAME TEXT UNIQUE
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS EMPLOYEE_SKILL (
    EMP_ID INTEGER,
    SKILL_ID INTEGER,
    LEVEL TEXT,
    FOREIGN KEY (EMP_ID) REFERENCES EMPLOYEE(EMP_ID),
    FOREIGN KEY (SKILL_ID) REFERENCES SKILL(SKILL_ID)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS ATTENDANCE (
    ATTENDANCE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    EMP_ID INTEGER,
    DATE TEXT,
    STATUS TEXT,
    FOREIGN KEY (EMP_ID) REFERENCES EMPLOYEE(EMP_ID)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS LEAVE_REQUEST (
    REQUEST_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    EMP_ID INTEGER,
    START_DATE TEXT,
    END_DATE TEXT,
    REASON TEXT,
    STATUS TEXT,
    FOREIGN KEY (EMP_ID) REFERENCES EMPLOYEE(EMP_ID)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS PAYROLL (
    PAYROLL_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    EMP_ID INTEGER,
    PAY_DATE TEXT,
    BASIC REAL,
    BONUS REAL,
    DEDUCTIONS REAL,
    FOREIGN KEY (EMP_ID) REFERENCES EMPLOYEE(EMP_ID)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS PERFORMANCE_REVIEW (
    REVIEW_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    EMP_ID INTEGER,
    REVIEW_DATE TEXT,
    RATING INTEGER,
    COMMENTS TEXT,
    FOREIGN KEY (EMP_ID) REFERENCES EMPLOYEE(EMP_ID)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS TRAINING (
    TRAINING_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    TITLE TEXT,
    START_DATE TEXT,
    END_DATE TEXT,
    TRAINER TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS EMPLOYEE_TRAINING (
    EMP_ID INTEGER,
    TRAINING_ID INTEGER,
    COMPLETION_STATUS TEXT,
    FOREIGN KEY (EMP_ID) REFERENCES EMPLOYEE(EMP_ID),
    FOREIGN KEY (TRAINING_ID) REFERENCES TRAINING(TRAINING_ID)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS ASSET (
    ASSET_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME TEXT,
    TYPE TEXT,
    EMP_ID INTEGER,
    ASSIGNED_DATE TEXT,
    FOREIGN KEY (EMP_ID) REFERENCES EMPLOYEE(EMP_ID)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS MEETING (
    MEETING_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    SUBJECT TEXT,
    DATE TEXT,
    TIME TEXT,
    DEPT_ID INTEGER,
    FOREIGN KEY (DEPT_ID) REFERENCES DEPARTMENT(DEPT_ID)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS EMPLOYEE_MEETING (
    EMP_ID INTEGER,
    MEETING_ID INTEGER,
    ATTENDANCE_STATUS TEXT,
    FOREIGN KEY (EMP_ID) REFERENCES EMPLOYEE(EMP_ID),
    FOREIGN KEY (MEETING_ID) REFERENCES MEETING(MEETING_ID)
);
""")

# 1. DEPARTMENT
departments = [
    ("Engineering", "Alice Johnson"),
    ("Human Resources", "Bob Smith"),
    ("Sales", "Carol Lee"),
    ("Marketing", "David Kim"),
    ("Finance", "Eva Brown")
]
cursor.executemany("INSERT INTO DEPARTMENT (DEPT_NAME, MANAGER_NAME) VALUES (?, ?)", departments)

# 2. EMPLOYEE
positions = ["Software Engineer", "HR Specialist", "Sales Executive", "Marketing Analyst", "Accountant"]
genders = ["Male", "Female", "Other"]
employees = []
for _ in range(100):
    name = faker.name()
    age = random.randint(22, 60)
    gender = random.choice(genders)
    position = random.choice(positions)
    salary = round(random.uniform(40000, 120000), 2)
    dept_id = random.randint(1, 5)
    email = faker.email()
    employees.append((name, age, gender, position, salary, dept_id, email))
cursor.executemany("""
    INSERT INTO EMPLOYEE (NAME, AGE, GENDER, POSITION, SALARY, DEPT_ID, EMAIL) 
    VALUES (?, ?, ?, ?, ?, ?, ?)""", employees)

# 3. PROJECT
projects = []
for i in range(20):
    name = f"{faker.bs().title()} Project"
    start_date = faker.date_between(start_date="-6M", end_date="today")
    end_date = faker.date_between(start_date=start_date, end_date="+6M")
    budget = round(random.uniform(10000, 100000), 2)
    dept_id = random.randint(1, 5)
    projects.append((name, str(start_date), str(end_date), budget, dept_id))
cursor.executemany("""
    INSERT INTO PROJECT (PROJECT_NAME, START_DATE, END_DATE, BUDGET, DEPT_ID) 
    VALUES (?, ?, ?, ?, ?)""", projects)

# 4. ASSIGNMENT
assignments = []
for emp_id in range(1, 101):
    for _ in range(random.randint(1, 3)):
        proj_id = random.randint(1, 20)
        role = random.choice(["Developer", "Analyst", "Lead", "Coordinator"])
        hours = random.randint(10, 40)
        assignments.append((emp_id, proj_id, role, hours))
cursor.executemany("""
    INSERT INTO ASSIGNMENT (EMP_ID, PROJECT_ID, ROLE, HOURS_PER_WEEK)
    VALUES (?, ?, ?, ?)""", assignments)

# 5. SKILL
skill_names = ["Python", "Excel", "Leadership", "Project Management", "SQL", "Communication", "Data Analysis",
               "Cloud Computing", "Networking", "Cybersecurity", "Machine Learning", "Negotiation", "Public Speaking",
               "ReactJS", "Django", "Java", "C++", "Docker", "Git", "Time Management", "Kubernetes", "HR Policies",
               "Financial Analysis", "Sales Strategy", "Market Research", "Graphic Design", "Content Writing",
               "NoSQL", "AWS", "Azure"]
cursor.executemany("INSERT INTO SKILL (SKILL_NAME) VALUES (?)", [(s,) for s in skill_names])

# 6. EMPLOYEE_SKILL
skills_map = []
for emp_id in range(1, 101):
    skill_ids = random.sample(range(1, 31), random.randint(2, 6))
    for skill_id in skill_ids:
        level = random.choice(["Beginner", "Intermediate", "Advanced"])
        skills_map.append((emp_id, skill_id, level))
cursor.executemany("""
    INSERT INTO EMPLOYEE_SKILL (EMP_ID, SKILL_ID, LEVEL)
    VALUES (?, ?, ?)""", skills_map)

# 7. ATTENDANCE
attendance_status = ["Present", "Absent", "Remote", "On Leave"]
attendance_data = []
for emp_id in range(1, 101):
    for _ in range(random.randint(5, 10)):
        date = faker.date_between(start_date="-30d", end_date="today")
        status = random.choice(attendance_status)
        attendance_data.append((emp_id, str(date), status))
cursor.executemany("""
    INSERT INTO ATTENDANCE (EMP_ID, DATE, STATUS)
    VALUES (?, ?, ?)""", attendance_data)

# 8. LEAVE_REQUEST
leave_requests = []
for _ in range(50):
    emp_id = random.randint(1, 100)
    start = faker.date_between(start_date="-60d", end_date="+10d")
    end = start + timedelta(days=random.randint(1, 5))
    reason = faker.sentence(nb_words=5)
    status = random.choice(["Approved", "Pending", "Rejected"])
    leave_requests.append((emp_id, str(start), str(end), reason, status))
cursor.executemany("""
    INSERT INTO LEAVE_REQUEST (EMP_ID, START_DATE, END_DATE, REASON, STATUS)
    VALUES (?, ?, ?, ?, ?)""", leave_requests)

# 9. PAYROLL
payrolls = []
for emp_id in range(1, 101):
    date = faker.date_between(start_date="-60d", end_date="today")
    basic = round(random.uniform(3000, 10000), 2)
    bonus = round(random.uniform(500, 2000), 2)
    deductions = round(random.uniform(100, 500), 2)
    payrolls.append((emp_id, str(date), basic, bonus, deductions))
cursor.executemany("""
    INSERT INTO PAYROLL (EMP_ID, PAY_DATE, BASIC, BONUS, DEDUCTIONS)
    VALUES (?, ?, ?, ?, ?)""", payrolls)

# 10. PERFORMANCE_REVIEW
reviews = []
for emp_id in range(1, 101):
    date = faker.date_between(start_date="-1y", end_date="today")
    rating = random.randint(1, 5)
    comments = faker.sentence(nb_words=10)
    reviews.append((emp_id, str(date), rating, comments))
cursor.executemany("""
    INSERT INTO PERFORMANCE_REVIEW (EMP_ID, REVIEW_DATE, RATING, COMMENTS)
    VALUES (?, ?, ?, ?)""", reviews)

# 11. TRAINING
trainings = []
for _ in range(10):
    title = faker.bs().title()
    start = faker.date_between(start_date="-90d", end_date="-10d")
    end = start + timedelta(days=random.randint(1, 5))
    trainer = faker.name()
    trainings.append((title, str(start), str(end), trainer))
cursor.executemany("""
    INSERT INTO TRAINING (TITLE, START_DATE, END_DATE, TRAINER)
    VALUES (?, ?, ?, ?)""", trainings)

# 12. EMPLOYEE_TRAINING
training_map = []
for emp_id in range(1, 101):
    training_ids = random.sample(range(1, 11), random.randint(1, 3))
    for t_id in training_ids:
        status = random.choice(["Completed", "Ongoing", "Not Started"])
        training_map.append((emp_id, t_id, status))
cursor.executemany("""
    INSERT INTO EMPLOYEE_TRAINING (EMP_ID, TRAINING_ID, COMPLETION_STATUS)
    VALUES (?, ?, ?)""", training_map)

# 13. ASSET
assets = []
for _ in range(50):
    name = faker.word().capitalize()
    type_ = random.choice(["Laptop", "Phone", "Monitor", "Tablet"])
    emp_id = random.randint(1, 100)
    date = faker.date_between(start_date="-6M", end_date="today")
    assets.append((name, type_, emp_id, str(date)))
cursor.executemany("""
    INSERT INTO ASSET (NAME, TYPE, EMP_ID, ASSIGNED_DATE)
    VALUES (?, ?, ?, ?)""", assets)

# 14. MEETING
meetings = []
for _ in range(20):
    subject = faker.bs().capitalize()
    date = faker.date_between(start_date="-30d", end_date="+30d")
    time = f"{random.randint(9,17)}:{random.choice(['00','30'])}"
    dept_id = random.randint(1, 5)
    meetings.append((subject, str(date), time, dept_id))
cursor.executemany("""
    INSERT INTO MEETING (SUBJECT, DATE, TIME, DEPT_ID)
    VALUES (?, ?, ?, ?)""", meetings)

# 15. EMPLOYEE_MEETING
emp_meetings = []
for emp_id in range(1, 101):
    meeting_ids = random.sample(range(1, 21), random.randint(1, 3))
    for m_id in meeting_ids:
        status = random.choice(["Attended", "Missed"])
        emp_meetings.append((emp_id, m_id, status))
cursor.executemany("""
    INSERT INTO EMPLOYEE_MEETING (EMP_ID, MEETING_ID, ATTENDANCE_STATUS)
    VALUES (?, ?, ?)""", emp_meetings)

# Commit everything
conn.commit()
conn.close()
print("✅ All tables populated with realistic sample data.")