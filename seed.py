import logging

from faker import Faker
from random import randint
from db import session

from models import Grade, Group, Subject, Student, Teacher



NUMBER_OF_GROUPS = 3
NUMBER_OF_STUDENTS = 40
NUMBER_OF_SUBJECTS = 8
NUMBER_OF_TEACHERS = 4
NUMBER_OF_GRADES = 20
SUBJECTS = ['Mathematics', 'History', 'Computer Science', 'Biology', 'Chemistry', 'Literature', 'Physics',
                    'Geography']



def insert_data():
    data = Faker()
    for i in range(NUMBER_OF_TEACHERS):
        teacher = Teacher(full_name=data.name())
        session.add(teacher)
    session.commit()

    for i in range(NUMBER_OF_GROUPS):
        group = Group(name=chr(65 + i))
        session.add(group)
    session.commit()

    for i in range(NUMBER_OF_STUDENTS):
        student = Student(full_name=data.name(), date_of_birth=data.date_of_birth(),
                          group_id=randint(1, NUMBER_OF_GROUPS))
        session.add(student)
    session.commit()

    for subject in SUBJECTS:
        subject = Subject(subject_name=subject, teacher_id = randint(1, NUMBER_OF_TEACHERS))
        session.add(subject)
    session.commit()

    for i in range(1,1+NUMBER_OF_STUDENTS):
        for j in range(1,1+NUMBER_OF_SUBJECTS):
            for k in range(NUMBER_OF_GRADES):
                grade = Grade(student_id=i, subject_id=j, grade=randint(1,100), date_received=data.date_between('-9w'))
                session.add(grade)
    session.commit()




if __name__ == '__main__':
    insert_data()