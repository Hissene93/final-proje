from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.forms import CourseForm, GradeForm
from app import bcrypt
from app.models import User, Student, Course, Grade

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/home')
def home():
    return render_template('home.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('main.admin_dashboard'))
    elif current_user.role == 'teacher':
        return redirect(url_for('main.teacher_dashboard'))
    else:
        return redirect(url_for('main.student_dashboard'))
  

@main_bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('main.home'))
    
    stats = {
        'students': Student.query.count(),
        'courses': Course.query.count(),
        'teachers': User.query.filter_by(role='teacher').count()
    }
    return render_template('admin/dashboard.html', stats=stats)

@main_bp.route('/admin/students')
@login_required
def manage_students():
    if current_user.role != 'admin':
        return redirect(url_for('main.home'))
    
    students = Student.query.all()
    return render_template('admin/students.html', students=students)

@main_bp.route('/admin/courses', methods=['GET', 'POST'])
@login_required
def manage_courses():
    if current_user.role != 'admin':
        return redirect(url_for('main.home'))
    
    form = CourseForm()
    teachers = User.query.filter_by(role='teacher').all()
    form.teacher.choices = [(t.id, f"{t.username}") for t in teachers]
    
    if form.validate_on_submit():
        course = Course(
            name=form.name.data,
            teacher_id=form.teacher.data,
            credits=form.credits.data
        )
        db.session.add(course)
        db.session.commit()
        flash('Cours ajouté avec succès!', 'success')
        return redirect(url_for('main.manage_courses'))
    
    courses = Course.query.all()
    return render_template('admin/courses.html', form=form, courses=courses)

@main_bp.route('/admin/grades', methods=['GET', 'POST'])
@login_required
def manage_grades():
    if current_user.role != 'admin':
        return redirect(url_for('main.home'))
    
    form = GradeForm()
    form.student.choices = [(s.id, f"{s.first_name} {s.last_name}") for s in Student.query.all()]
    form.course.choices = [(c.id, c.name) for c in Course.query.all()]
    
    if form.validate_on_submit():
        grade = Grade(
            student_id=form.student.data,
            course_id=form.course.data,
            grade=form.grade.data
        )
        db.session.add(grade)
        db.session.commit()
        flash('Note enregistrée avec succès!', 'success')
        return redirect(url_for('main.manage_grades'))
    
    grades = Grade.query.all()
    return render_template('admin/grades.html', form=form, grades=grades)


@main_bp.route('/teacher/dashboard')
@login_required
def teacher_dashboard():
    if current_user.role != 'teacher':
        return redirect(url_for('main.home'))
    
    courses = Course.query.filter_by(teacher_id=current_user.id).all()
    return render_template('teacher/dashboard.html', courses=courses)


@main_bp.route('/student/dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        return redirect(url_for('main.home'))
    
    student = Student.query.filter_by(user_id=current_user.id).first()
    if not student:
        flash('Profil étudiant non trouvé', 'danger')
        return redirect(url_for('main.home'))
    
    grades = Grade.query.filter_by(student_id=student.id).all()
    return render_template('student/dashboard.html', student=student, grades=grades)

@main_bp.route('/admin/students/add', methods=['POST'])
@login_required
def add_student():
    if current_user.role != 'admin':
        return redirect(url_for('main.home'))
    
    
    username = request.form.get('username')
    email = request.form.get('email')
    
    
    
    hashed_pw = bcrypt.generate_password_hash('password123').decode('utf-8')
    user = User(username=username, email=email, password=hashed_pw, role='student')
    db.session.add(user)
    db.session.commit()
    
    student = Student(
        first_name=request.form.get('first_name'),
        last_name=request.form.get('last_name'),
        user_id=user.id
    )
    db.session.add(student)
    db.session.commit()
    
    flash('Étudiant ajouté avec succès!', 'success')
    return redirect(url_for('main.manage_students'))