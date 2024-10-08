print('começando routes')
from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.forms import RegisterForm, LoginForm, PostForm, SearchForm
from app.models import Users, Posts
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, LoginManager, logout_user, current_user
from werkzeug.utils import secure_filename
import uuid as uuid
import os

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html')

# Create Register Page
@app.route("/register", methods=['GET', 'POST'])
def register():
    name = None
    password_hash = None
    form = RegisterForm()
    # Validate Form
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash Password
            hashed_password = generate_password_hash(form.password_hash.data, "pbkdf2:sha256")
            user = Users(username=form.username.data, name=form.name.data, email=form.email.data, password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
            print('Registration Successful! Please Log In.')
            return redirect(url_for('login'))
        name = form.name.data
        password_hash = form.password_hash.data
        form.username.data = ''
        form.name.data = ''
        form.email.data = ''
        form.password_hash.data = ''
    our_users = Users.query.order_by(Users.date_added)
    return render_template('register.html', name = name, password_hash = password_hash, form = form, our_users = our_users)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    next_page = request.args.get('next')
    if next_page == '/' or next_page == '/home':
        print('TRUE')

    # Validate Form
    print(form.validate_on_submit())
    if form.validate_on_submit():
        print('yeah!')
        user = Users.query.filter_by(username=form.username.data).first()
        print(user)
        if user:
            #check the hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                print('login sucessful')
                return redirect(url_for('posts'))
            else:
                print('wrong password')
        else:
            print('that user doesn\'t exist')
    logout_user()
    return render_template('login.html', form=form)

#criando o logout
@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    print('logout sucedido')
    return redirect(url_for('login'))

@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    form = RegisterForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form.get('name')
        name_to_update.username = request.form.get('username')
        name_to_update.email = request.form.get('email')
        # Check for profile pic
        if request.files.get('profile_pic'):
            name_to_update.profile_pic = request.files.get('profile_pic')
            # Grab Image Name
            pic_filename = secure_filename(name_to_update.profile_pic.filename)
            # Set UUID
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            # Save Image
            name_to_update.profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
            # Change to text to save to db
            name_to_update.profile_pic = pic_name
            try:
                db.session.commit()
                flash("User Updated Successfully!")
                return render_template('dashboard.html', name_to_update = name_to_update, form = form)
            except:
                flash("Whoops! There Was A Problem Updating The User!")
                return render_template('dashboard.html', name_to_update = name_to_update, form = form)
        else:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template('dashboard.html', name_to_update = name_to_update, form = form)
    else:
        return render_template('dashboard.html', name_to_update = name_to_update, form = form)

# Create Update User Profile Page
@app.route('/update_profile/<int:id>', methods=['GET', 'POST'])
def update_profile(id):
    form = RegisterForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form.get('name')
        name_to_update.username = request.form.get('username')
        name_to_update.email = request.form.get('email')
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template('update_profile.html', name_to_update = name_to_update, form = form)
        except:
            flash("Whoops! There Was A Problem Updating The User!")
            return render_template('update_profile.html', name_to_update = name_to_update, form = form)
    else:
        return render_template('update_profile.html', name_to_update = name_to_update, form = form)

# Create Delete User Page
@app.route('/delete/<int:id>')
@login_required
def delete(id):
    if current_user.id == id or current_user.id == 1:
        user_to_delete = Users.query.get_or_404(id)
        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("User Deleted Successfully!")
            
            # Keep admin on database page
            if current_user.id == 1:
                return redirect(url_for('database'))
            else:
                return redirect(url_for('register'))
        except Exception as e:
            flash(f"Whoops! There Was A Problem Deleting The User: {str(e)}")
            return redirect(url_for('dashboard'))
    else:
        flash("Sorry, You Don't Have Permission To Delete This User!")
        return redirect(url_for('dashboard'))


    
# Create Add Posts Page
@app.route('/add-post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        poster = current_user.id
        post = Posts(title=form.title.data, content=form.content.data, poster_id=poster)
        # Add post data to db
        db.session.add(post)
        db.session.commit()
        flash("Post Submitted Successfully!")
        return redirect(url_for('posts'))
    return render_template("add_post.html", form = form)

# Create View Posts Page
@app.route('/posts')
def posts():
    # Get posts from db
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts)

# Create View Individual Post Page
@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)

# Create Edit Post Page
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        # Update db
        db.session.add(post)
        db.session.commit()
        flash("Post Updated Successfully!")
        return redirect(url_for('post', id=post.id))
    if current_user.id == post.poster_id or current_user.id == 1:
        form.title.data = post.title
        form.content.data = post.content
        return render_template('edit_post.html', form=form)
    else:
        flash("You're Not Authorized To Edit That Post!")
        return render_template('post.html', post=post)

# Create Delete Post Page
@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    id = current_user.id
    if id == post_to_delete.poster.id or id == 1:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            flash("Post Deleted Successfully!")
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("posts.html", posts=posts)
        except:
            flash("Whoops! There Was A Problem Deleting The Post!")
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("posts.html", posts=posts)
    else:
        flash("You're Not Authorized To Delete That Post!")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)

# Pass Stuff To Navbar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

# Create Search Function
@app.route('/search', methods=["POST"])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        # Get data from form submitted
        post.searched = form.searched.data
        # Query the database
        posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
        posts = posts.order_by(Posts.title).all()
        return render_template("search.html", form=form, searched=post.searched, posts=posts)
    
@app.route('/admin')
@login_required
def admin():
    id = current_user.id
    if id == 1:
        return render_template("admin.html")
    else:
        return redirect(url_for('home'))
    
@app.route('/admin/database', methods=['GET', 'POST'])
@login_required
def database():
    # Verify if the user is an admin
    if current_user.id != 1:
        flash("You're not authorized to access this page!")
        return redirect(url_for('home'))
    # Query the database for users and posts
    all_users = Users.query.order_by(Users.date_added).all()
    all_posts = Posts.query.order_by(Posts.date_posted).all()
    return render_template('database.html', users=all_users, posts=all_posts)


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