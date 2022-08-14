from db_connect import db
import datetime


student_lesson = db.Table(
   'student_lesson',
   db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
   db.Column('lesson_id', db.Integer, db.ForeignKey('lessons.id')))


class Student(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(20), nullable=False)
    number = db.Column('number', db.String(4), unique=True, nullable=False)
    age = db.Column('age', db.Integer, nullable=False)
    _class = db.Column('class', db.String(4), nullable=False)

    def __init__(self, name, number, age, _class) -> None:
        self.name = name
        self.number = number
        self.age = age
        self._class = _class

    def __repr__(self) -> str:
        return self.name


class Lessons(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    lesson_name = db.Column('lesson_name', db.String(20),
                            unique=True, nullable=False)
    teacher_name = db.Column('teacher_name', db.String(20), nullable=False)
    student = db.relationship('Student', secondary=student_lesson)

    def __init__(self, lesson_name, teacher_name) -> None:
        self.lesson_name = lesson_name
        self.teacher_name = teacher_name

    def __repr__(self) -> str:
        return self.lesson_name


class Grades(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    midterm = db.Column('midterm', db.Integer, nullable=False)
    final = db.Column('final', db.Integer, nullable=False)
    student_id = db.Column('student_id', db.ForeignKey('student.id'))
    lesson_id = db.Column('lesson_id', db.ForeignKey('lessons.id'))

    def __init__(self, midterm, final, student_id, lesson_id) -> None:
        self.midterm = midterm
        self.final = final
        self.student_id = student_id
        self.lesson_id = lesson_id


class Logs(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    log = db.Column('log', db.String(60), nullable=False)

    def __init__(self, log) -> None:
        self.log = log

    def create_log(model: str, _type: str, *args: list[str]) -> str:
        date = datetime.datetime.now().strftime("%d.%m.%Y  %H:%M:%S")
        # ADD: add lesson or student
        if _type == 'ADD':
            desc = f"{args[0]} has been created"
        # ASL: add student to lesson
        elif _type == 'ASL':
            desc = f"Person {args[0]} has been added to Lesson {args[1]}"
        # ANS: add note to student
        elif _type == 'ANS':
            desc = (
                f"Person {args[0]} has been added grade of midterm "
                f"{args[2]} and grade of final {args[3]} in Lesson {args[1]}")
        elif model == 'Student_lesson' and _type == 'DEL':
            desc = (
                f"Student ID {args[0]} and Lesson ID {args[1]} has "
                f"been deleted from {model} table")
        elif model == 'Grades' and _type == 'DEL':
            f"Grades ID {args[0]} has been deleted"
        elif _type == 'DEL':
            desc = f"{args[0]} has been deleted"
        return f"{date} - {model} - {_type} - {desc}"


# db.drop_all()
db.create_all()
