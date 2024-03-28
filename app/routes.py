from flask import request
from . import app
from datetime import datetime
from hw_data.tasks import tasks_list

@app.route('/tasks')
def get_tasks():
    # Get the posts from storage (fake data -> tomorrow will be db)
    tasks = tasks_list
    return tasks

@app.route('/tasks/<int:task_id>')
def get_task(task_id):
    # Get the posts from storage
    tasks = tasks_list
    # For each dictionary in the list of post dictionaries
    for task in tasks:
        # If the key of 'id' matches the post_id from the URL
        if task['id'] == task_id:
            # Return that post dictionary
            return task
    # If we loop through all of the posts without returning, the post with that ID does not exist
    return {'error': f"Post with an ID of {task_id} does not exist"}, 404

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
        return {'error': f"{', '.join(missing_fields)}must be in the body"},400
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

