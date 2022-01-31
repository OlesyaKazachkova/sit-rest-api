from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from config import Configuration
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Configuration)
auth = HTTPBasicAuth()
db = SQLAlchemy(app)

# Initial commit 3
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(256), unique=False, nullable=False)
    todo_list = db.relationship('Todo', backref='user', lazy='dynamic')


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), db.ForeignKey('users.username'))
    task_name = db.Column(db.String(128), nullable=False)
    task_status = db.Column(db.Boolean(), default=False, nullable=False)


@auth.verify_password
def verify_password(username, password):
    user = db.session.query(User).filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        return username


@app.route('/')
@auth.login_required
def index():
    return jsonify({'users': auth.current_user()})


# Создание пользователя
@app.route('/user/add', methods=['POST'])
def user():
    hashed_password = generate_password_hash(request.form['password'], method='sha256')
    new_user = User(name=request.form['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created!'})


# Вывод всех задач для авторизованного пользователя
@app.route('/todo', methods=['GET'])
@auth.login_required
def get_all():
    data = Todo.query.filter_by(username=auth.current_user()).all()

    output = []

    for todo in data:
        todo_data = {}
        todo_data['id'] = todo.id
        todo_data['task_name'] = todo.task_name
        todo_data['complete'] = todo.task_status
        output.append(todo_data)

    return jsonify({'todos': output})


# Добавление задачи
@app.route('/todo', methods=['POST'])
@auth.login_required
def create_todo():
    new_todo = Todo(username=auth.current_user(), task_name=request.form['task_name'])
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({'message': 'Todo created!'})


# Обновить статус задачи
@app.route('/todo/<task_id>', methods=['PUT'])
@auth.login_required
def change_todo(task_id):
    todo = Todo.query.filter_by(username=auth.current_user(), id=task_id).first()

    if not todo:
        return jsonify({'message': 'No todo found'})

    todo.task_status = request.form['task_status'] == 'True'
    db.session.commit()

    return jsonify({'message': 'Todo item has been completed!'})


# Удалить задачу
@app.route('/todo/<task_id>', methods=['DELETE'])
@auth.login_required
def delete_todo(task_id):
    todo = Todo.query.filter_by(username=auth.current_user(), id=task_id).first()

    if not todo:
        return jsonify({'message': 'No todo found'})

    db.session.query(Todo).filter_by(username=auth.current_user(), id=task_id).delete()
    db.session.commit()

    return jsonify({'message': 'Todo item deleted!'})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
