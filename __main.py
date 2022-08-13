from db_connect import db,app
from models import Grades, Student, Lessons, Logs, create_log
from flask import render_template, url_for, redirect, request
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

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
