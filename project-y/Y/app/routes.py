print('começando routes')
from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.forms import Register, Login
from app.models import Users
from werkzeug.security import generate_password_hash

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('home.html')

# Create Register Page
@app.route("/register", methods=['GET', 'POST'])
def register():
    name = None
    password_hash = None
    form = Register()
    # Validate Form
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash Password
            hashed_password = generate_password_hash(form.password_hash.data, "pbkdf2:sha256")
            user = Users(name=form.name.data, email=form.email.data, password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        password_hash = form.password_hash.data
        form.name.data = ''
        form.email.data = ''
        form.password_hash.data = ''
        flash("Registration Form Submitted Successfully")
    our_users = Users.query.order_by(Users.date_added)
    #if se for post e tiver os argumentos certos, redirect to login
    return render_template('register.html', name = name, password_hash = password_hash, form = form, our_users = our_users)

@app.route("/login", methods=['GET', 'POST'])
def login():
    email = None
    password = None
    form = Login()
    # Validate Form
    if form.validate_on_submit():
        email = form.email.data
        form.email.data = ''
        password = form.password.data
        form.password.data = ''
    #if se for post e tiver os argumentos certos, redirect to home
    return render_template('login.html', email = email, password = password, form = form)

# Create User Profile Page
@app.route('/user_profile/<int:id>', methods=['GET', 'POST'])
def user_profile(id):
    form = Register()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form.get('name')
        name_to_update.email = request.form.get('email')
        name_to_update.password = request.form.get('password')  
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template('user_profile.html', name_to_update = name_to_update, form = form)
        except:
            flash("Whoops! There Was A Problem Updating The User!")
            return render_template('user_profile.html', name_to_update = name_to_update, form = form)
    else:
        return render_template('user_profile.html', name_to_update = name_to_update, form = form)

# Create Delete User Page
@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    password_hash = None
    form = Register()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!")
        our_users = Users.query.order_by(Users.date_added)
        return render_template('register.html', name = name, password_hash = password_hash, form = form, our_users = our_users)
    except:
        flash("Whoops! There Was A Problem Deleting The User!")
        return render_template('register.html', name = name, password_hash = password_hash, form = form, our_users = our_users)

@app.route("/logout")
def logout():
    return redirect(url_for('login'))

@app.route("/like/<int:post_id>", methods=['POST'])
def like_post(post_id):
    # post = Post.query.get_or_404(post_id)
    # if post.likes.filter_by(user_id=current_user.id).first():
    #     like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    #     db.session.delete(like)
    # else:
    #     like = Like(user_id=current_user.id, post_id=post_id)
    #     db.session.add(like)
    # db.session.commit()
    return redirect(url_for('home'))

print('terminando routes')