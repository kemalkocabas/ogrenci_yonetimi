from db_connect import db,app
from models import Grades, Student, Lessons, Logs, create_log
from flask import render_template, url_for, redirect, request
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError


@app.route('/')
def show_students():
   student_list = Student.query.all()
   return render_template('student_list.html', student_list=student_list)


@app.route('/add_student', methods = ['GET', 'POST'])
def add_student():
   try:
      if request.method == 'POST':   
         student = Student(request.form['name'], request.form['number'], request.form['age'], request.form['class'])      
         db.session.add(student)
         log = create_log('Student', 'ADD', request.form['name'])
         db.session.add(Logs(log))        
         db.session.commit()

         return redirect(url_for('show_students'))
      return render_template('add_student.html')
   except IntegrityError:
         message= "This number of student has already been entered "
         return render_template('add_student.html', message=message)


@app.route("/add_lesson", methods=['GET', 'POST'])
def add_lesson():
   if request.method == 'POST':
      lesson_list = Lessons.query.filter(Lessons.lesson_name == request.form['name']).all()
      if lesson_list:
         message = "The lesson has already been added"
         return render_template('add_lesson.html', message=message)                          
      lesson = Lessons(request.form['name'], request.form['teacher_name'])
      log = create_log('Lessons', 'ADD', request.form['name'])
      db.session.add(lesson)
      db.session.add(Logs(log))
      db.session.commit()
      return redirect(url_for('show_lessons'))
   return render_template('add_lesson.html')


@app.route("/add_student_lesson", methods=['GET', 'POST'])
def add_student_lesson():
   lesson_list = db.session.query(Lessons.lesson_name).distinct().all()
   student_list = Student.query.all()
   teacher = None
   if request.method == 'POST':
      teacher = db.session.query(Lessons.teacher_name).filter(Lessons.lesson_name == request.form['lesson_name']).all()[0].teacher_name
      checklist = request.form.getlist('get_students')
      for check in checklist:
         control = Lessons.query.filter(Lessons.lesson_name == request.form['lesson_name'], Lessons.student_id == check).all()
         if control:
            message = "This lesson has already been added"
            return render_template("add_student_lesson.html",lesson_list=lesson_list, teacher=teacher, student_list=student_list, message=message)
       
         lesson = Lessons(request.form['lesson_name'], teacher, check)
         db.session.add(lesson)
         student_name = Student.query.filter(Student.id == check).all()[0]
         print(student_name)
         log = create_log('Lessons', 'ASL', student_name, request.form['lesson_name'])
         db.session.add(Logs(log))
         Lessons.query.filter(and_(Lessons.lesson_name == request.form['lesson_name'], Lessons.student_id == None)).delete()
      db.session.commit()         
      return redirect(url_for('show_student_by_lesson'))
   return render_template("add_student_lesson.html",lesson_list=lesson_list, teacher=teacher, student_list=student_list)

@app.route('/show_lessons')
def show_lessons():
   lesson_list = db.session.query(Lessons.id, Lessons.lesson_name, Lessons.teacher_name).distinct().all()
   return render_template('lesson_list.html', lesson_list=lesson_list)

@app.route('/student_list_by_lessons', methods=['GET','POST'])
def show_student_by_lesson():
   lesson = request.form.get('lesson_name')
   lesson_list = db.session.query(Lessons.lesson_name).distinct().all()
   student_list = Student.query.join(Lessons).add_columns(Student.id, Student.name, Student.number, Student.age, Student._class, Lessons.lesson_name, Lessons.teacher_name).filter(Student.id == Lessons.student_id).filter(Lessons.lesson_name == lesson)  
   return render_template('student_list_by_lesson.html', student_list=student_list, lesson_list=lesson_list, lesson=lesson)

@app.route('/student_details/<number>')
def student_details(number):
   student = db.session.query(Student.id, Student.name).filter(Student.number == number).one()
   query = db.session.query(Student, Lessons, Grades).add_columns(Student.name, Lessons.lesson_name, Grades.midterm, Grades.final).filter(Student.id == Lessons.student_id, Lessons.id == Grades.lesson_id, Student.number == number)
   return render_template('student_details.html', number=number, student=student, query=query)

@app.route('/notes')
def show_notes():
   query = Grades.query.all()
   return render_template('student_details.html',query=query)


   
@app.route('/add_notes/<number>', methods=['GET','POST'])
def add_notes(number):
   student = db.session.query(Student.id, Student.name).filter(Student.number == number).one()
   lesson_list = db.session.query(Lessons.id, Lessons.lesson_name).filter(Lessons.student_id == student.id)
   
   if request.method == 'POST':
      control = Grades.query.filter(Grades.lesson_id == request.form['lesson_name'], Grades.student_id == student.id).all()
      if control:
         message = "Grades have already been added"
         return render_template('add_notes.html', student=student, lesson_list=lesson_list, message=message)

      grades = Grades(request.form['midterm'], request.form['final'], student.id, request.form['lesson_name'])
      lesson_name = Lessons.query.filter(Lessons.id == request.form['lesson_name']).all()[0]
      log = create_log('Grades','ANS',student.name, lesson_name , request.form['midterm'], request.form['final'])
      db.session.add(grades)
      db.session.add(Logs(log))
      db.session.commit()
      return redirect(url_for('student_details', number=number))
   
   return render_template('add_notes.html', student=student, lesson_list=lesson_list)

@app.route('/delete_student/<number>', methods=['GET'])
def delete_student(number):
   student_id = db.session.query(Student.id).filter(Student.number == number)[0][0]
   Student.query.filter(Student.number == number).delete()
   Lessons.query.filter(Lessons.student_id == student_id).delete()
   Grades.query.filter(Grades.student_id == student_id).delete()
   db.session.commit()
   return redirect(url_for('show_students', number=number))


@app.route('/delete_lesson/<id>', methods=['GET'])
def delete_lesson(id):
   Lessons.query.filter(Lessons.id == id).delete()
   Grades.query.filter(Grades.lesson_id == id).delete()
   db.session.commit()
   return redirect(url_for('show_lessons'))   
   
@app.route('/logs')
def logs():
   logs = Logs.query.all()
   return render_template('logs.html', logs=logs)

app.run(debug=True, use_reloader=True)
