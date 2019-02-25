from app import app, db
from app.models import User, Post
import os

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

dirName = 'app/zapis'
try:
    os.mkdir(dirName)
    print("Directory ", dirName, " Created ")
except FileExistsError:
    print("Directory ", dirName, " already exists")