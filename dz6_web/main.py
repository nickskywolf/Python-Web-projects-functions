from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from faker import Faker
import random
from datetime import date

# Створення бази даних та сесії
engine = create_engine('sqlite:///students.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Створення таблиць
class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    group_id = Column(Integer, ForeignKey('groups.id'))
    scores = relationship('Score', back_populates='student')
    group = relationship('Group', back_populates='students')

# В класі Group додайте back_populates для subjects
class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    students = relationship('Student', back_populates='group')
    subjects = relationship('Subject', secondary='subject_group', back_populates='groups')

# В класі Subject додайте back_populates для groups
class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    scores = relationship('Score', back_populates='subject')
    teacher = relationship('Teacher', back_populates='subjects')
    groups = relationship('Group', secondary='subject_group', back_populates='subjects')


class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    subjects = relationship('Subject', back_populates='teacher')

class Score(Base):
    __tablename__ = 'scores'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    score = Column(Float)
    date = Column(Date)
    student = relationship('Student', back_populates='scores')
    subject = relationship('Subject', back_populates='scores')

# Створення таблиці для зв'язку між предметами та групами
subject_group = Table('subject_group', Base.metadata,
    Column('group_id', Integer, ForeignKey('groups.id')),
    Column('subject_id', Integer, ForeignKey('subjects.id'))
)

Base.metadata.create_all(engine)

# Заповнення таблиць випадковими даними
fake = Faker()
groups = []
subjects = []
teachers = []
students = []

# Створення груп
for _ in range(3):
    group = Group(name=fake.word())
    groups.append(group)

# Створення викладачів
for _ in range(4):
    teacher = Teacher(name=fake.name())
    teachers.append(teacher)

# Створення предметів та призначення викладачів
for _ in range(8):
    subject = Subject(name=fake.word())
    subject.teacher_id = random.choice(teachers).id
    subjects.append(subject)

# Створення студентів та призначення груп
for _ in range(50):
    student = Student(name=fake.name())
    student.group_id = random.choice(groups).id
    students.append(student)

# Додавання оцінок
for student in students:
    for subject in subjects:
        score = Score(score=random.uniform(2, 5), date=fake.date_between(start_date='-1y', end_date='today'))
        score.student = student
        score.subject = subject
        session.add(score)

session.commit()
