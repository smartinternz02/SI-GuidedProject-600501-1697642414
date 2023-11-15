import secrets
import os
# import tensorflow
from tensorflow import keras
import numpy as np
from flask import render_template, url_for, flash, redirect, request
from detection import app, db, bcrypt
from detection.forms import RegistrationForm,LoginForm, UploadForm
from detection.models import User, Upload
from flask_login import login_user, current_user, logout_user, login_required

model = keras.models.load_model(r"xrayprediction.h5", compile=False)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home')) 
        else:
            flash('Login Unsuccessful. Please check the credentials', 'danger')

    return render_template('login.html', title='Login', form=form)

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user= User(username=form.username.data, email=form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    image_file = url_for('static', filename='profile_pic/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file= image_file)

@app.route('/upload')
def uploadpage():
    return render_template("upload.html")


@app.route('/upload', methods=['GET', 'Post'])
def upload():
    print(request.files)
    if request.method == 'POST':
        f = request.files['imagefile']
        basepath = os.path.dirname(__file__)
        filepath = os.path.join(basepath, 'uploads', f.filename)
        f.save(filepath)


        img = keras.preprocessing.image.load_img(
            filepath, target_size=(64, 64))
        x = keras.preprocessing.image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        pred = np.argmax(model.predict(x), axis=1)
       
        index = ['Covid', 'Lung Opacity', 'Normal ', 'Viral Pneumonia']
        diagnosis = "The diagnosis is:"+str(index[pred[0]])


    return render_template("upload.html",prediction=diagnosis)




# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(app.root_path, 'static/xraypic', picture_fn)
#     form_picture.save(picture_path)

#     return picture_fn


# @app.route("/xrayup", methods = ['GET', 'POST'])
# @login_required
# def xrayup():
#     form = UploadForm()
#     if form.validate_on_submit():
#         upload = Upload(title=form.title.data, picture = form.upload_image.data, paitent=current_user)
#         db.session.add(post)
#         db.session.commit()
#         if form.picture.data:
#             picture_file = save_picture(form.picture.data)
#         flash(f'Upload Successful', 'success')
#         return redirect(url_for('home'))
#     return render_template('xrayup.html', title='Upload', form=form)


# @app.route('/upload', methods=['GET', 'Post'])
# def upload():
#     print(request.files)
#     if request.method == 'POST':
#         f = request.files['imagefile']
#         basepath = os.path.dirname(__file__)
#         filepath = os.path.join(basepath, 'uploads', f.filename)
#         f.save(filepath)

#         img = keras.preprocessing.image.load_img(
#             filepath, target_size=(64, 64))
#         x = keras.preprocessing.image.img_to_array(img)
#         x = np.expand_dims(x, axis=0)
#         pred = np.argmax(model.predict(x), axis=1)
        
#         index = ['Covid', 'Lung Opacity', 'Normal ', 'Viral Pneumonia']
#         diagnosis = "The diagnosis is:"+str(index[pred[0]])

#     return render_template("Upload.html",prediction=diagnosis)