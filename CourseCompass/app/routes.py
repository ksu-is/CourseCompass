from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from app.models import db, User, Grade
from flask_mail import Message
from app import mail
from app.decorators import admin_required  # ✅ New import

def register_routes(app):

    @app.route('/')
    def home():
        return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                flash("Login successful", "success")
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid credentials", "danger")
                return redirect(url_for('login'))

        return render_template("login.html")

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == "POST":
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]

            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash("Username already taken. Please choose another one.", "danger")
                return redirect(url_for("register"))

            hashed_pw = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()

            msg = Message(
                subject='Welcome to CourseCompass 🎓',
                sender='coursecompass@outlook.com',
                recipients=[email],
                body=f"Hi {username},\n\nThank you for registering at CourseCompass!"
            )
            mail.send(msg)

            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("login"))

        return render_template("register.html")

    @app.route('/dashboard')
    @login_required
    def dashboard():
        grades = current_user.grades
        if grades:
            avg = round(sum(g.grade for g in grades) / len(grades), 2)
            if avg >= 90:
                letter = 'A'
            elif avg >= 80:
                letter = 'B'
            elif avg >= 70:
                letter = 'C'
            elif avg >= 60:
                letter = 'D'
            else:
                letter = 'F'
        else:
            avg = None
            letter = None

        return render_template("dashboard.html", user=current_user, grades=grades, avg=avg, letter=letter)

    @app.route('/add', methods=['GET', 'POST'])
    @login_required
    def add_grade():
        if request.method == 'POST':
            course_name = request.form['course_name']
            grade = float(request.form['grade'])
            new_grade = Grade(course_name=course_name, grade=grade, user_id=current_user.id)
            db.session.add(new_grade)
            db.session.commit()
            flash('Grade added successfully.', 'success')
            return redirect(url_for('dashboard'))
        return render_template('add_grade.html')

    @app.route('/edit/<int:grade_id>', methods=['GET', 'POST'])
    @login_required
    def edit_grade(grade_id):
        grade = Grade.query.get_or_404(grade_id)
        if grade.user_id != current_user.id:
            flash("Access denied.", "danger")
            return redirect(url_for('dashboard'))

        if request.method == 'POST':
            grade.course_name = request.form['course_name']
            grade.grade = float(request.form['grade'])
            db.session.commit()
            flash("Grade updated successfully.", "success")
            return redirect(url_for('dashboard'))

        return render_template("edit_grade.html", grade=grade)

    @app.route('/delete/<int:grade_id>', methods=['POST', 'GET'])
    @login_required
    def delete_grade(grade_id):
        grade = Grade.query.get_or_404(grade_id)
        if grade.user_id != current_user.id:
            flash("Access denied.", "danger")
            return redirect(url_for('dashboard'))

        db.session.delete(grade)
        db.session.commit()
        flash("Grade deleted.", "info")
        return redirect(url_for('dashboard'))

    @app.route('/admin')
    @login_required
    @admin_required
    def admin_dashboard():
        users = User.query.all()
        return render_template("admin_dashboard.html", users=users)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash("You have been logged out.", "info")
        return redirect(url_for('login'))
