from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Task
from datetime import datetime,date

task_routes = Blueprint('tasks', __name__)

VALID_STATUSES = {'todo', 'doing', 'done'}
VALID_PRIORITIES = {'low', 'normal', 'high'}


# ======== Task ROUTES ========
@task_routes.route('/task', methods=['GET'])
def server():
    return({"message": " task router"})


@task_routes.route('/tasks', methods=['POST'])
def create_task():
    if 'user_id' not in session:
        return jsonify({"error": "Login required"}), 401

    data = request.json
    title = data.get('title')
    due_date_str = data.get('due_date')
    status = data.get('status', 'todo')
    priority = data.get('priority', 'normal')

    # Validation
    if not title:
        return jsonify({"error": "Title is required"}), 400
    if status not in VALID_STATUSES:
        return jsonify({"error": f"Invalid status, must be one of {VALID_STATUSES}"}), 400
    if priority not in VALID_PRIORITIES:
        return jsonify({"error": f"Invalid priority, must be one of {VALID_PRIORITIES}"}), 400

    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
            if due_date.date() < date.today():
                return jsonify({"error": "Due date must be today or in the future"}), 400
        except ValueError:
            return jsonify({"error": "Invalid due_date format, use YYYY-MM-DD"}), 400

    new_task = Task(
        title=title,
        description=data.get('description', ''),
        due_date=due_date,
        status=status,
        priority=priority,
        owner_id=session['user_id']
    )
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"id": new_task.id, "message": "Task created"}), 201


# List Tasks
@task_routes.route('/tasks', methods=['GET'])
def get_tasks():
    if 'user_id' not in session:
        return jsonify({"error": "Login required"}), 401
    
    tasks = Task.query.filter_by(owner_id=session['user_id']).all()
    
    return jsonify([
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "due_date": str(t.due_date) if t.due_date else None,
            "status": t.status,
            "priority": t.priority,
            "created_at": str(t.created_at) if t.created_at else None
        }
        for t in tasks
    ])


# Get Task by ID
@task_routes.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    if 'user_id' not in session:
        return jsonify({"error": "Login required"}), 401

    task = Task.query.get_or_404(id)
    if task.owner_id != session['user_id']:
        return jsonify({"error": "Not authorized"}), 403

    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "due_date":  str(task.due_date) if task.due_date else None,
        "status": task.status,
        "priority": task.priority,
        "created_at": str(task.created_at) if task.created_at else None
    })


# Update Task 
@task_routes.route('/tasks/<int:id>', methods=['PATCH'])
def update_task(id):
    if 'user_id' not in session:
        return jsonify({"error": "Login required"}), 401

    task = Task.query.get_or_404(id)
    if task.owner_id != session['user_id']:
        return jsonify({"error": "Not authorized"}), 403

    data = request.get_json() or {}

    if 'title' in data:
        if not data['title']:
            return jsonify({"error": "Title cannot be empty"}), 400
        task.title = data['title']

    if 'description' in data:
        task.description = data['description']

    if 'status' in data:
        if data['status'] not in VALID_STATUSES:
            return jsonify({"error": f"Invalid status, must be one of {VALID_STATUSES}"}), 400
        task.status = data['status']

    if 'priority' in data:
        if data['priority'] not in VALID_PRIORITIES:
            return jsonify({"error": f"Invalid priority, must be one of {VALID_PRIORITIES}"}), 400
        task.priority = data['priority']

    if 'due_date' in data:
        try:
            due_date = datetime.strptime(data['due_date'], "%Y-%m-%d")
            if due_date.date() < date.today():
                return jsonify({"error": "Due date must be today or in the future"}), 400
            task.due_date = due_date
        except ValueError:
            return jsonify({"error": "Invalid due_date format, use YYYY-MM-DD"}), 400

    db.session.commit()
    return jsonify({"message": "Task updated"})


# Delete Task 
@task_routes.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    if 'user_id' not in session:
        return jsonify({"error": "Login required"}), 401

    task = Task.query.get_or_404(id)
    if task.owner_id != session['user_id']:
        return jsonify({"error": "Not authorized"}), 403

    db.session.delete(task)
    db.session.commit()
    return '', 204