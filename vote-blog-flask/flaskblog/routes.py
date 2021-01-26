import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             PostForm, RequestResetForm, ResetPasswordForm, GenForm)
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import cv2
import numpy as np
import pickle
from PIL import Image
import numpy as np
import time
import random
import pymysql

def pathss(st):
    path = os.path.join(app.root_path, 'static/',st)
    return path

def getface(valtbc):
    #print("1")
    face_cascade = cv2.CascadeClassifier(pathss('face\\HCTrainingImages\\haarcascade_frontalface_default.xml'))

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(pathss('face\\training.yml'))
    iddict = pickle.load(open(pathss('face\\pickle\\iddict.pkl'),'rb'))
    font = cv2.FONT_HERSHEY_SIMPLEX
    cap = cv2.VideoCapture(0)
    start_time = time.asctime(time.localtime(time.time()))

    att_stud = {}
    init_faculty = {}
    facenum = 0
    arrn=[]
    #print("2")
    while facenum<50:

        _, img = cap.read()
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(grey, 1.3, 5)

        for (x,y,w,h) in faces:
            roi_grey = grey[y:y+h, x:x+w]
            pred_id, config = recognizer.predict(roi_grey)


            facenum+=1
            
            for regno,[id,desig] in iddict.items():
                if id == pred_id:
                    pred_regno = regno
            arrn+=[pred_regno]        
            #print(pred_regno)    
            colour_desig = tuple([255 if desig == 'student' else 0, 255 if desig == 'faculty' else 0,255 if desig == 'admin' else 0])
            cv2.putText(img, str(pred_regno), (x,y), font , 1, colour_desig, 2)
            #cv2.putText(img, str(desig), (x,y+h), font , 1, colour_desig, 2)
            #cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
            cv2.circle(img, (int(x+w/2),int(y+h/2)), int(h/2), (0,255,0), 2)

            """if regno not in att_stud and desig == 'student':
                                        att_stud[regno] = [desig, time.asctime(time.localtime(time.time()))]
                            
                                    if regno not in init_faculty and desig == 'faculty':
                                        init_faculty[regno] = [desig, time.asctime(time.localtime(time.time()))]"""

        cv2.imshow('img', img)
        k = cv2.waitKey(30) &0xFF
        if k==27:
               break

    cap.release()
    cv2.destroyAllWindows()
    end_time = time.asctime(time.localtime(time.time()))

    all_att = []
    if os.path.exists('face\\pickle\\all_att.pkl'):
        all_att = pickle.load(open(pathss('face\\pickle\\all_att.pkl'), 'rb'))

    all_att.append([att_stud, init_faculty, start_time, end_time])
    pickle.dump(all_att,open(pathss('face\\pickle\\all_att.pkl'),'wb'))
    #print("3")
    return arrn.count(valtbc)

def train():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    im_path = [pathss('face\\UserFaces\\student') , pathss('face\\UserFaces\\faculty') , pathss('face\\UserFaces\\admin')]
    im_path_all = []
    for i in im_path:
        for j in os.listdir(i):
            im_path_all.append(i + '\\' + j)


    def getImagesId(path):
        imagepaths_1 = []
        for path in im_path_all:
            if len(os.listdir(path))>0:
                imagepaths_1.append([os.path.join(path, imageid) for imageid in os.listdir(path)])


            imagepaths = []
            for sublist in imagepaths_1:
                for item in sublist:
                    imagepaths.append(item)
            faces = []
            ids = []
            desig = []
            desig.append(path.split('\\')[2+6])
            print(path)
            for imagepath in imagepaths:
                faceimg = Image.open(imagepath).convert('L')
                npface = np.array(faceimg,'uint8')
                #print(str(imagepath))
                #print(os.path.split(imagepath)[0].split('\\'))
                ID = os.path.split(imagepath)[0].split('\\')[-1]
                print(ID)
                faces.append(npface)
                ids.append(ID)

        return(faces, ids, desig)

    faces,ids,desig = getImagesId(im_path)
    index = 0
    iddict = {}
    train_ID = []
    for id in ids:
        if id not in iddict:
            iddict[id]=[index, desig[0]]
            index+=1
    for id in ids:
        train_ID.append(iddict.get(id)[0])


    pickle.dump(iddict,open(pathss('face\\pickle\\iddict.pkl'),'wb'))

    recognizer.train(faces, np.array(train_ID))
    recognizer.save(pathss('face\\training.yml'))
    cv2.destroyAllWindows()

def newUser(id):
    category_path = {1:'student' , 2:'faculty' , 3:'admin'}
    #id = input('Enter register number: ')
    #picture_path = os.path.join(app.root_path, 'static/profile_pics')
    os.mkdir (pathss('face\\UserFaces\\' + str(category_path[1]) +'\\' + str(id)))
    cap = cv2.VideoCapture(0)

    face_cascade = cv2.CascadeClassifier(pathss('face\\HCTrainingImages\\haarcascade_frontalface_default.xml'))
    #eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    facenum = 0

    while True:

        _, img = cap.read()
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(grey, 1.3, 5)

        for (x,y,w,h) in faces:
            roi_grey = grey[y:y+h, x:x+w]
            facenum += 1
            cv2.imwrite(pathss('face\\UserFaces\\' + str(category_path[1]) +'\\' + str(id) + '\\' + str(facenum) + '.jpg'), roi_grey)
            cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
    ##        roi_color = img[y:y+h, x:x+w]
    ##        eyes = eye_cascade.detectMultiScale(roi_grey)
    ##        for (ex, ey, ew, eh) in eyes:
    ##            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0,255,0), 2)

        cv2.imshow('img', img)
        if facenum == 50:
            break
        k = cv2.waitKey(30) &0xFF
        if k==27:
               break


    cap.release()
    cv2.destroyAllWindows()


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        newUser(form.email.data)
        train()
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    print("0")
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    print("00")
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if getface(form.email.data)>40 and user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

@app.route("/card",methods=["POST","GET"])
@login_required
def card():
    return render_template('card.html', title='card no')



# this part of code is for randomkey generator
def get_rows():
    em=current_user.email
    connection = pymysql.connect(host="127.0.0.1",user="root",passwd="",database="voter" )
    cursor = connection.cursor()
    retrive = "Select * from vote where ID='"+em+"';"
    #executing the quires
    cursor.execute(retrive)
    rows = cursor.fetchall()
    connection.commit()
    connection.close()
    return rows

def insert_into_db(ID,KEYCODE):
    connection = pymysql.connect(host="127.0.0.1",user="root",passwd="",database="voter" )
    cursor = connection.cursor()
    insert1 = "INSERT INTO vote VALUES('"+ID+"','"+KEYCODE+"',1);"
    cursor.execute(insert1)
    connection.commit()
    connection.close()

def get_code():
    em=current_user.email
    rows=get_rows()
    if(len(rows)==0):
        KEYCODE=''.join([random.choice("12345667890ABCDEF12345667890GHIJKLMNOPQRST12345667890") for i in range(20) ])
        insert_into_db(em,KEYCODE)
        return KEYCODE

def gen(code="Not Generated"):
    #code="123123"
    return render_template('cgen.html', title='Account',code=code)

@app.route("/gene",methods=["POST","GET"])
@login_required
def gene():

    if len(get_rows())!=0:
        row=get_rows()[0]
        code=row[1]
        voted=row[2]
        if voted==1:
            code+='  (CODE GENERATED PREVIOUSLY)'
        else:
            code+='  (ALREADY VOTED)'
        return gen(code)       

    form = GenForm()
    if form.validate_on_submit():
        if form.etype.data=="I ACCEPT" :
            next_page = request.args.get('next')
            code=get_code()
            return gen(code)
            #return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Enter the correct phase', 'danger')
    return render_template('generate.html', title='Login', form=form)