import os


class Configuration(object):
    file_path = os.path.abspath(os.getcwd()) + "/todo.db"
    SECRET_KEY = '...'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + file_path
