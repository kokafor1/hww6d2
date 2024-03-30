from flask import request
from . import app, db
from .models import Task
from datetime import datetime
from hw_data.tasks import tasks_list

@app.route('/tasks')
def get_tasks():
    if not request.is_json:
        return {'error': 'Your content-type must be a json'}, 400
    data = request.json
    required_fields = ['title', 'description']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
    
    title = data.get('title')
    description = data.get('description')

    new_task = Task(title = title, description = description)

    return new_task.to_dict(), 201


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
    title = data['title']
    description = data['description']

    new_task = {
        "id": len(tasks_list) + 1,
        "title": data['title'],
        "description": data['description'],
        "completed": False,
        "dateCreated": data.get('date_created')
    }

    tasks_list.append(new_task)

    return data

