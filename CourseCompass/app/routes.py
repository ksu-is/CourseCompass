def register_routes(app):  # 👈 Level 0
    @app.route('/register', methods=['GET', 'POST'])  # 👈 Level 1 (indented 4 spaces or 1 tab)
    def register():
        if request.method == "POST":
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]

            # Check if user already exists
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash("Username already taken. Please choose another one.", "danger")
                return redirect(url_for("register"))

            hashed_pw = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()

            # Send welcome email
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
