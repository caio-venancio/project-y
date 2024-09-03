print('começando routes')
from flask import render_template, url_for, flash, redirect, request
from app import app

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login.html')

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