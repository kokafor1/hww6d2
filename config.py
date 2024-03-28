import os

# Get the base directory of this folder
basedir = os.path.abspath(os.path.dirname(__file__))
# "C:\Users\bstan\Documents\codingtemple-kekambas-142\week6\flask-blog-api"

class Config:
    FLASK_APP = os.environ.get('FLASK_APP')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')