

from flask import render_template, flash, redirect, url_for, request, session, escape
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from app import app, db
from app.forms import LoginForm, RegistrationForm,makeF,delF
from app.models import User
import os
import os.path
from flask_autoindex import AutoIndex


files_index = AutoIndex(app, os.path.curdir + '/app/zapis', add_url_rules=False)

@app.route('/asd/',methods = ['POST', 'GET'])
@app.route('/asd/<path:path>',methods = ['POST', 'GET'])
@login_required
def autoindex(path=''):

    form = makeF()
    if form.validate_on_submit():
        dirName = 'app/zapis/' +session['username']+'/'+ path+'/'+form.tekst.data
        try:
            os.mkdir(dirName)
            print("Directory ", dirName, " Created ")
        except FileExistsError:
            print("Directory ", dirName, " already exists")
        return redirect(request.url)


#    form2 = delF()
#    if form2.validate_on_submit() :
#        print('dziala')
#        return redirect(request.url)


    if request.method =='POST':
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            UPLOAD_FOLDER = 'app/zapis/' + session['username'] +"/"+path
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return redirect(request.url)

    print(request.method + "Metoda")

    if request.method == 'GET':
        print(request.form.get('hiddenName'))
        UPLOAD_FOLDER = 'app/zapis/' + session['username'] + "/" + path
        print(UPLOAD_FOLDER)
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        f = open(os.path.join(app.config['UPLOAD_FOLDER'],"nazwa"),"w+")
        f.write("PLIK")
        f.close()

        form2 = delF()
   #     if form2.validate_on_submit() || request.form.get('')




#       return redirect(request.url)


    return files_index.render_autoindex(path,os.path.curdir + '/app/zapis/' + session['username'],template_context = dict(form=form))



@app.route('/user/<username>')
@login_required
def user(username):
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')



@app.route('/')
@app.route('/checkb')
@login_required
def checkb():
    return render_template('checkbo.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        session['username'] = request.form['username']
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index',form=form)
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Udalo ci sie zarejestrować')
        us_name = form.username.data
        dirName = (('app/zapis/' + us_name),('app/zapis/' + us_name + '/Documents'),('app/zapis/' + us_name + '/Photos'))
        for i in dirName:
            os.mkdir(i)
        return redirect(url_for('login'))
    return render_template('register.html',title='Rejestracja',form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))