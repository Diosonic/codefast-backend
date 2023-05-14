import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Database Options
    MYSQL_HOST= 'localhost'
    MYSQL_USER= 'root'
    MYSQL_PASSWORD= '734946'
    MYSQL_DB= 'root'
    MYSQL_PORT= '3306'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:734946@localhost/codefast'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_HEADERS = 'Content-Type'
    PORT = "8000"

