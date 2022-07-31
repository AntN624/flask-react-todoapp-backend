from audioop import cross
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from datetime import datetime

app = Flask(__name__)

env = 'prod'

if (env == 'prod'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://qhtatjdiubecwb:73305923f31658f0c6c4a2086ef334bb505a2ad00cd489037442c1999b5bf8c7@ec2-44-206-197-71.compute-1.amazonaws.com:5432/d6ld7eujiu72t0'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Cool@localhost/flask-react-todoapp'

db = SQLAlchemy(app)
CORS(app)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'Todo: {self.description}'

    def __init__(self, task):
        self.task = task

def formatter(todo):
    return (
        {
            'id':todo.id,
            'task':todo.task,
            'created_at':todo.created_at
        }
    )

@app.route('/')
@cross_origin()
def main():
    return 'hi'

# get all todo tasks
@app.route('/todos', methods=['GET'])
@cross_origin()
def get_todos():
    todos = ToDo.query.order_by(ToDo.created_at.asc()).all()
    all_todos = []
    for todo in todos:
        all_todos.append(formatter(todo))
    return {'todos':all_todos}

# get a single todo
@app.route('/todos/<id>', methods=['GET'])
@cross_origin()
def get_todo(id):
    todo = ToDo.query.filter_by(id=id).one()
    formatted = formatter(todo)
    return(
        {
            "todo":formatted
        }
    )

# create a new todo
@app.route('/todos', methods=['POST'])
@cross_origin()
def create_todo():
    task = request.json['newTask']
    todo = ToDo(task)
    db.session.add(todo)
    db.session.commit()
    return formatter(todo)

# delete todos
@app.route('/todos/<id>', methods=['DELETE'])
@cross_origin()
def delete_todo(id):
    todo = ToDo.query.filter_by(id=id).one()
    db.session.delete(todo)
    db.session.commit()
    return f'{todo.task} task deleted'

# edit todo
@app.route('/todos/<id>', methods=['PUT'])
@cross_origin()
def edit_todo(id):
    todo = ToDo.query.filter_by(id=id)
    task = request.json['task']
    todo.update(dict(task = task, created_at=datetime.utcnow()))
    db.session.commit()
    return {'todo': formatter(todo.one())}