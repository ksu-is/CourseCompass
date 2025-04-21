from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message

from app.models import User, Grade
from app import db, mail, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def register_routes(app):

    @app.route('/')
    def index():
        return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('dashboard'))
            flash('Invalid credentials')
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        grades = Grade.query.filter_by(user_id=current_user.id).all()
        if grades:
            avg = round(sum(g.grade for g in grades) / len(grades), 2)
            letter = (
                'A' if avg >= 90 else
                'B' if avg >= 80 else
                'C' if avg >= 70 else
                'D' if avg >= 60 else
                'F'
            )
        else:
            avg = None
            letter = None

        return render_template('dashboard.html', grades=grades, avg=avg, letter=letter)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('Username already exists. Please choose another.')
                return redirect(url_for('register'))

            hashed_pw = generate_password_hash(password)
            new_user = User(username=username, password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()

            msg = Message(
                subject='Welcome to CourseCompass 🎓',
                sender='coursecompass@outlook.com',
                recipients=[f"{new_user.username}@students.kennesaw.edu"],
                body=f"Hi {new_user.username},\n\nThank you for registering at CourseCompass!"
            )
            mail.send(msg)

            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/add-grade', methods=['GET', 'POST'])
    @login_required
    def add_grade():
        if request.method == 'POST':
            course_name = request.form.get('course_name')
            grade = request.form.get('grade')
            if course_name and grade:
                try:
                    new_grade = Grade(course_name=course_name, grade=float(grade), user_id=current_user.id)
                    db.session.add(new_grade)
                    db.session.commit()
                    flash('Grade added successfully!')
                    return redirect(url_for('dashboard'))
                except ValueError:
                    flash("Please enter a valid number.")
            else:
                flash("All fields are required.")
        return render_template('add_grade.html')

    @app.route('/edit-grade/<int:grade_id>', methods=['GET', 'POST'])
    @login_required
    def edit_grade(grade_id):
        grade = Grade.query.get_or_404(grade_id)
        if grade.user_id != current_user.id:
            flash("You don't have permission to edit this grade.")
            return redirect(url_for('dashboard'))

        if request.method == 'POST':
            grade.course_name = request.form['course_name']
            grade.grade = float(request.form['grade'])
            db.session.commit()
            flash('Grade updated successfully!')
            return redirect(url_for('dashboard'))

        return render_template('edit_grade.html', grade=grade)

    @app.route('/delete-grade/<int:grade_id>')
    @login_required
    def delete_grade(grade_id):
        grade = Grade.query.get_or_404(grade_id)
        if grade.user_id != current_user.id:
            flash("You don't have permission to delete this grade.")
            return redirect(url_for('dashboard'))

        db.session.delete(grade)
        db.session.commit()
        flash('Grade deleted successfully.')
        return redirect(url_for('dashboard'))
