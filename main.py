from db_connect import db,app
from models import Grades, Student, Lessons, Logs
from flask import render_template, url_for, redirect, request
from sqlalchemy.exc import IntegrityError


@app.route('/')
def show_students() -> str:
   student_list = Student.query.all()
   print(type(render_template('student_list.html', student_list=student_list)))
   return render_template('student_list.html', student_list=student_list)


@app.route('/add_student', methods = ['GET', 'POST'])
def add_student() -> str:
   try:
      if request.method == 'POST':   
         student = Student(request.form['name'], request.form['number'], request.form['age'], request.form['class'])      
         db.session.add(student)
         log = Logs.create_log('Student', 'ADD', request.form['name'])
         db.session.add(Logs(log))        
         db.session.commit()
         return redirect(url_for('show_students'))
      return render_template('add_student.html')
   except IntegrityError:
         message= "This number of student has already been entered "
         return render_template('add_student.html', message=message)



@app.route("/add_lesson", methods=['GET', 'POST'])
def add_lesson() -> str:
   try:
      if request.method == 'POST':               
         lesson = Lessons(request.form['name'], request.form['teacher_name'])
         db.session.add(lesson)
         log = Logs.create_log('Lessons', 'ADD', request.form['name'])
         db.session.add(Logs(log))
         db.session.commit()
         return redirect(url_for('show_lessons'))
      return render_template('add_lesson.html')
   except IntegrityError:
      message = "The lesson has already been added"
      return render_template('add_lesson.html', message=message) 


@app.route("/add_student_lesson", methods=['GET', 'POST'])
def add_student_lesson() -> str:
   lesson_list = Lessons.query.all()
   student_list = Student.query.all()
   if request.method == 'POST':
      checklist = request.form.getlist('get_students')
      lesson_id = request.form['lesson_name']
      
      lesson = Lessons.query.filter(Lessons.id == lesson_id).all()
      for check in checklist:
         student = Student.query.filter(Student.id == check).all()
         lesson[0].student.append(student[0])
         db.session.add(lesson[0])
         log = Logs.create_log('Student_lesson', 'ASL', student[0].name, lesson[0].lesson_name)
         db.session.add(Logs(log))
      db.session.commit()
      return redirect(url_for('show_student_by_lesson')) 
   return render_template("add_student_lesson.html",lesson_list=lesson_list, student_list=student_list)


@app.route('/show_lessons')
def show_lessons() -> str:
   lesson_list = db.session.query(Lessons.id, Lessons.lesson_name, Lessons.teacher_name).all()
   return render_template('lesson_list.html', lesson_list=lesson_list)

@app.route('/student_list_by_lessons', methods=['GET','POST'])
def show_student_by_lesson() -> str:
   lesson = request.form.get('lesson_name')
   lesson_list = db.session.query(Lessons.lesson_name).all()
   student_list = Student.query.join(Lessons.student).filter(Lessons.lesson_name == lesson).all()
   return render_template('student_list_by_lesson.html', student_list=student_list, lesson_list=lesson_list, lesson=lesson)


@app.route('/student_details/<number>')
def student_details(number) -> str:
   student = db.session.query(Student.id, Student.name).filter(Student.number == number).one()
   query = db.session.query(Student, Lessons, Grades).add_columns(Lessons.lesson_name, Grades.midterm, Grades.final).filter(Lessons.id == Grades.lesson_id, Student.id == Grades.student_id, Grades.student_id == student.id).all()
   return render_template('student_details.html', number=number, student=student, query=query)


   
@app.route('/add_notes/<number>', methods=['GET','POST'])
def add_notes(number: str) -> str:
   student = db.session.query(Student.id, Student.name).filter(Student.number == number).one()
   lesson_list = Lessons.query.join(Lessons.student).filter(student.id == student.id)
   
   if request.method == 'POST':
      control = Grades.query.filter(Grades.lesson_id == request.form['lesson_name'], Grades.student_id == student.id).all()
      if control:
         message = "Grades have already been added"
         return render_template('add_notes.html', student=student, lesson_list=lesson_list, message=message)

      grades = Grades(request.form['midterm'], request.form['final'], student.id, request.form['lesson_name'])
      lesson_name = Lessons.query.filter(Lessons.id == request.form['lesson_name']).all()[0]
      log = Logs.create_log('Grades','ANS',student.name, lesson_name , request.form['midterm'], request.form['final'])
      db.session.add(grades)
      db.session.add(Logs(log))
      db.session.commit()
      return redirect(url_for('student_details', number=number))   
   return render_template('add_notes.html', student=student, lesson_list=lesson_list)


@app.route('/delete_student/<number>', methods=['GET'])
def delete_student(number: str) -> str:
   student_id = db.session.query(Student.id).filter(Student.number == number).one()[0]
   student = Student.query.filter(Student.id == student_id).all()[0]
   
   lesson_list = Lessons.query.join(Lessons.student).filter(Student.id == student_id).all()
   if lesson_list:
      lesson_list[0].student.remove(student)
      log = Logs.create_log('Student_lesson', 'DEL', student_id, lesson_list[0].id)
      db.session.add(Logs(log))

   Student.query.filter(Student.number == number).delete()
   student_log = Logs.create_log('Student', 'DEL', student.name)
   grade = Grades.query.filter(Grades.student_id == student_id).all()
   grade_log = Logs.create_log('Grades', 'DEL', grade[0].id)
   Grades.query.filter(Grades.student_id == student_id).delete()
   db.session.add(Logs(student_log))
   db.session.add(Logs(grade_log))
   db.session.commit()
   return redirect(url_for('show_students'))


@app.route('/delete_lesson/<id>', methods=['GET'])
def delete_lesson(id: str) -> str:
   lesson = Lessons.query.join(Lessons.student).filter(Lessons.id == id).all()
   student = Student.query.join(Lessons.student).filter(Lessons.id == id).all()
   if student:
      lesson[0].student.remove(student[0])
      log = Logs.create_log('Student_lesson', 'DEL', student[0].id, lesson[0].id)
      db.session.add(Logs(log))
   Lessons.query.filter(Lessons.id == id).delete()
   lesson_log = Logs.create_log('Lessons', 'DEL', lesson[0].lesson_name)
   db.session.add(Logs(lesson_log))
   Grades.query.filter(Grades.lesson_id == id).delete()
   grade_log = Logs.create_log('Grades', 'DEL', id)
   db.session.add(Logs(grade_log))
   db.session.commit()
   return redirect(url_for('show_lessons'))   
   
   
@app.route('/logs')
def logs() -> str:
   logs = Logs.query.all()
   return render_template('logs.html', logs=logs)


app.run(debug=True, use_reloader=True)
