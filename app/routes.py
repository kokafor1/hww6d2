from flask import request
from . import app, db
from .models import Task, User
from .auth import basic_auth, token_auth

@app.route('/')
def index():
    return "<h1>Hello World</h1>"

@app.route('/tasks/<int:task_id>')
def get_task(task_id):
    task = db.session.get(Task, task_id)
    if task:
        return task.to_dict()
    else:
        return {'error': f'Task with and ID of {task_id} does not exist'}, 404

@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.is_json:
        return {'error': 'Youre not doing it right'},400
    data = request.json
    required_fields = ['title', 'description']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)}must be in the description"},400
    title = data.get['title']
    description = data.get['description']

    current_user = token_auth.current_user()

    new_task = Task(title = title, description = description, user_id = current_user.id)

    return new_task.to_dict(), 201

@app.route('/users', methods=['POST'])
def create_user():
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    data = request.json

    required_fields = ['username', 'email', 'password']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    check_users = db.session.execute(db.select(User).where( (User.username == username) | (User.email == email) )).scalars().all()
    if check_users:
        return {'error': "A user with that username and/or email already exists"}, 400
    new_user = User(username = username , email = email, password = password)

    return new_user.to_dict(), 201

@app.route('/token')
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user()
    return user.get_token()

@app.route('/tasks')
def get_tasks():
    select_stmt = db.select(Task)
    search = request.args.get('search')
    if search:
        select_stmt = select_stmt.where(Task.title.ilike(f"%{search}%"))
    task = db.session.execute(select_stmt).scalars().all()
    return [t.to_dict() for t in task]

@app.route('/tasks/<int:task_id>', methods=['PUT'])
@token_auth.login_required
def edit_task(task_id):
    if not request.is_json:
        return {'error': 'You content-type must be application/json'}, 400
    task = db.session.get(Task, task_id)
    if task is None:
        return {'error': f"Post with ID #{task_id} does not exist"}, 404
    current_user = token_auth.current_user()
    if current_user is not task.author:
        return {'error': "This is not your post. You do not have permission to edit"}, 403
    
    data = request.json
    task.update(**data)
    return task.to_dict()

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@token_auth.login_required
def delete_task(task_id, user_id):
    task = db.session.get(Task, task_id)
    if task is None:
        return {'error': f"Post {task_id} does not exist"}, 404
    user = db.session.get(User, user_id )
    if task.user_id != user.id:
        return {'error' : f"Task #{task_id} is not associated with task #{user_id}"}, 403
    current_user = token_auth.current_user()
    if task.user != current_user:
        return {'error': 'You do not have permission to delete this comment'}, 403
    task.delete()
    return {'success': "Task has been successfully deleted"}, 200

@app.route('/users/<int:user_id>', methods=['DElETE'])
@basic_auth.login_required
def delete_user(user_id):
    user = db.session.get(User, user_id)
    user.delete()
    return {'success': 'User has been deleted'}, 200