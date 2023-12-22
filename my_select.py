from models import Grade, Student, Subject, Teacher, Group
from sqlalchemy import desc, func, select, and_
from db import session


def select_1():
    result = session.query(Student.id, Student.full_name, func.round(func.avg(Grade.grade), 2).label('Average grade')) \
        .select_from(Student).join(Grade).group_by(Student.id).order_by(desc('Average grade')).limit(5).all()
    return result


def select_2():
    result = session.query(Student.id, Student.full_name, func.round(func.avg(Grade.grade), 2).label('Average grade')) \
        .select_from(Student).join(Grade).where(Grade.subject_id == 2).group_by(Student.id) \
        .order_by(desc('Average grade')).limit(1).all()
    return result

def select_3():
    result = session.query(Group.name,func.round(func.avg(Grade.grade),2))\
        .select_from(Grade)\
        .join(Student, Grade.student_id == Student.id)\
        .join(Group, Student.group_id == Group.id)\
        .join(Subject, Grade.subject_id == Subject.id)\
        .where(Subject.id == 4)\
        .group_by(Group.name).all()
    return result

def select_4():
    result = session.query(func.round(func.avg(Grade.grade),2)).select_from(Grade).all()
    return result

def select_5():
    result = session.query(Teacher.full_name, Subject.subject_name)\
        .select_from(Teacher)\
        .join(Subject)\
        .where(Teacher.id == 4).all()
    return result

def select_6():
    result = session.query(Student.full_name.label('Student list')).where(Student.group_id == 1).all()
    return result

def select_7():
    result = session.query(Student.id, Student.full_name, func.round(func.avg(Grade.grade),2).label('average'))\
        .select_from(Student)\
        .join(Grade)\
        .join(Group)\
        .where(and_(Grade.subject_id == 2, Group.id == 2))\
        .group_by(Student.id)\
        .order_by(desc('average')).all()
    return result

def select_8():
    result = session.query(Teacher.full_name, func.round(func.avg(Grade.grade),2))\
        .select_from(Teacher)\
        .join(Subject)\
        .join(Grade)\
        .where(Teacher.id == 3)\
        .group_by(Teacher.full_name).all()
    return result

def select_9():
    result = session.query(Student.full_name, Subject.subject_name)\
        .select_from(Student)\
        .join(Grade)\
        .join(Subject)\
        .where(Student.id == 27)\
        .group_by(Student.full_name, Subject.subject_name).all()
    return result

def select_10():
    result = session.query(Student.full_name, Subject.subject_name, Teacher.full_name)\
        .select_from(Student)\
        .join(Grade)\
        .join(Subject)\
        .join(Teacher)\
        .where(and_(Student.id == 17, Teacher.id == 4))\
        .group_by(Student.full_name, Subject.subject_name, Teacher.full_name).all()
    return result

def select_11():
    result = session.query(Teacher.full_name, Student.full_name, func.avg(Grade.grade))\
        .select_from(Grade)\
        .join(Student)\
        .join(Subject)\
        .join(Teacher)\
        .where(and_(Teacher.id == 4, Student.id == 31))\
        .group_by(Teacher.full_name, Student.full_name).all()
    return result

def select_12():
    subquery = (select(func.max(Grade.date_received))).scalar_subquery()

    result = session.query(Grade.id, Grade.grade)\
        .select_from(Grade)\
        .join(Student)\
        .join(Group)\
        .where(and_(Grade.date_received == subquery, Group.id == 1)).all()

    return result

if __name__ == '__main__':
    print(select_1())
    print(select_2())
    print(select_3())
    print(select_4())
    print(select_5())
    print(select_6())
    print(select_7())
    print(select_8())
    print(select_9())
    print(select_10())
    print(select_11())
    print(select_12())