print('começando routes')
from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.forms import Register, LoginForm, PostForm
from app.models import Users, Posts
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, LoginManager, logout_user, current_user

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
    form = Register()
    # Validate Form
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash Password
            hashed_password = generate_password_hash(form.password_hash.data, "pbkdf2:sha256")
            user = Users(username=form.username.data, name=form.name.data, email=form.email.data, password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
            print('User submited!')
        name = form.name.data
        password_hash = form.password_hash.data
        form.username.data = ''
        form.name.data = ''
        form.email.data = ''
        form.password_hash.data = ''
        flash("Registration Form Submitted Successfully!")
        # colocar um redirect aqui para login
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
                return redirect(url_for('home'))
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

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

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
        return redirect(url_for('register'))
    except:
        flash("Whoops! There Was A Problem Deleting The User!")
        return redirect(url_for('register'))
    
# Create Add Posts Page
@app.route('/add-post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(title=form.title.data, content=form.content.data, author=form.author.data, slug=form.slug.data)
        # Add post data to db
        db.session.add(post)
        db.session.commit()
        flash("Post Submitted Successfully!")
        return redirect(url_for('add_post'))
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
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        # Update db
        db.session.add(post)
        db.session.commit()
        flash("Post Updated Successfully!")
        return redirect(url_for('post', id=post.id))
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template('edit_post.html', form = form)

# Create Delete Post Page
@app.route('/posts/delete/<int:id>')
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
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