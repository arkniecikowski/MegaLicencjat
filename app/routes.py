

from flask import render_template, flash, redirect, url_for, request, session, escape
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename
from app import app, db
from app.forms import LoginForm, RegistrationForm, StworzFolderForm, DodajPlikForm
from app.models import User
import os
import shutil
from os import path
import os.path
from flask_autoindex import AutoIndex


def remove(path):
    """ param <path> could either be relative or absolute. """
    if os.path.isfile(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))



files_index = AutoIndex(app, os.path.curdir + '/app/zapis', add_url_rules=False)


@app.route('/asd/',methods = ['POST', 'GET'])
@app.route('/asd/<path:path>',methods = ['POST', 'GET'])
@login_required
def autoindex(path=''):

    form = StworzFolderForm(request.form)
    form2 = DodajPlikForm()

    if request.method == 'GET':

            if request.args.get('sub') == "Rename":

                flash("ZMIEN_NAZWE")

            if request.args.get('sub') == "Zmien":

                flash("Zmienokokookokkokokokoko")



    if request.method == 'POST' :

        if request.form['sub'] == "Usuń pliki":
            listaDoU = request.form.getlist('checkName')
            print(listaDoU)

            for r in listaDoU:
                wr = 'app/zapis/' + session['username'] + "/" + path + "/" + r
                if os.path.exists(wr) or os.path.isdir(wr):
                    remove(wr)

        elif  request.form['sub'] == "Stworz folder" and form.tekst.data != None:

            dirName = 'app/zapis/' +session['username']+'/'+ path+'/'+form.tekst.data
            try:
                os.mkdir(dirName)
                print("Directory ", dirName, " Created ")
            except FileExistsError:
                print("Directory ", dirName, " already exists")
            return redirect(request.url)

        elif request.form['sub'] == "Dodaj plik" and form2.plik.data != None:

            f = request.files['plik']
            filename = secure_filename(f.filename)
            UPLOAD_FOLDER = 'app/zapis/' + session['username'] + "/" + path
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(request.url)
            return redirect(request.url)

        elif request.form['sub'] == "Zmien to nazwe":
            t = request.form.get('modalRenameTextName')
            ch = request.form.get("checkName")

            src_ch = 'app/zapis/' +session['username']+'/'+ path+ch
            src_t = 'app/zapis/' +session['username']+'/'+ path+t
            try:
                os.rename(src_ch,src_t)
            except FileExistsError:
                print('nie udalo sie zmienic nazwy')
            return redirect(request.url)



    return files_index.render_autoindex(path,os.path.curdir + '/app/zapis/' + session['username'],template_context = dict(form=form,form2=form2))





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