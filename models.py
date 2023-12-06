from sqlalchemy import CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, sessionmaker, declarative_base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime



Base = declarative_base()
class Group(Base):
    __tablename__ = 'groups'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)

class Teacher(Base):
    __tablename__ = 'teachers'
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    full_name: Mapped[str] = mapped_column(nullable=False)

class Student(Base):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(nullable=False)
    date_of_birth = mapped_column(DateTime, nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey(Group.id, ondelete='CASCADE'))
    group = relationship('Group', backref='students')

class Subject(Base):
    __tablename__ = 'subjects'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    subject_name: Mapped[str] = mapped_column(nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey(Teacher.id, ondelete='CASCADE'))
    teacher = relationship('Teacher', backref='subjects')

class Grade(Base):
    __tablename__ = 'grades'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey(Student.id, ondelete='CASCADE'))
    subject_id: Mapped[int] = mapped_column(ForeignKey(Subject.id, ondelete='CASCADE'))
    grade: Mapped[int] = mapped_column(CheckConstraint('grade>=0 and grade<=100'))
    date_received = mapped_column(DateTime, nullable=False)
    student = relationship('Student', backref='grades')
    subject = relationship('Subject', backref='grades')





