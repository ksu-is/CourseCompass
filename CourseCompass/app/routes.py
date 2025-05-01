from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from app.models import db, User
from flask_mail import Message
from app import mail

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
        average = sum(g.score for g in grades) / len(grades)
    else:
        average = None
    return render_template("dashboard.html", user=current_user, grades=grades, average=average)


    @app.route('/add', methods=['GET', 'POST'])
    @login_required
    def add_grade():
        if request.method == 'POST':
        title = request.form['title']
        score = float(request.form['score'])
        new_grade = Grade(title=title, score=score, user_id=current_user.id)
        db.session.add(new_grade)
        db.session.commit()
        flash('Grade added successfully.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_grade.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash("You have been logged out.", "info")
        return redirect(url_for('login'))
