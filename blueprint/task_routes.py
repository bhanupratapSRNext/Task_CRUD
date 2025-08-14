from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import Task, User
from datetime import datetime
from flask import Blueprint, request, jsonify, render_template, redirect, url_for



task_routes = Blueprint("task_routes", __name__, template_folder="templates")

VALID_STATUS = {'todo', 'progress', 'done'}
VALID_PRIORITY = {'low', 'medium', 'high'}

# Helper: Pagination
def paginate(query):
    try:
        limit = int(request.args.get('limit', 20))
        offset = int(request.args.get('offset', 0))
        limit = min(limit, 100)
    except ValueError:
        limit = 20
        offset = 0
    return query.limit(limit).offset(offset).all()

# Helper: Task serialization
def serialize_task(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "status": task.status,
        "priority": task.priority,
        "owner_id": task.owner_id,
        "created_at": task.created_at.isoformat()
    }

#CRUD Routes #

# Create Task

# @task_routes.route("/tasks/create", methods=["GET", "POST"])
# def create_task():
#     if request.method == "GET":
#         # Show HTML form in browser
#         return render_template("task_create.html")

#     if request.content_type == "application/json":
#         # JSON request (API client)
#         data = request.get_json()
#     else:
#         # Form request (browser)
#         data = {
#             "title": request.form.get("title"),
#             "description": request.form.get("description"),
#             "status": request.form.get("status"),
#             "priority": request.form.get("priority"),
#         }

#     # Create task in DB
#     new_task = Task(
#         title=data.get("title"),
#         description=data.get("description"),
#         status=data.get("status", "pending"),
#         priority=data.get("priority", "medium"),
#     )
#     db.session.add(new_task)
#     db.session.commit()

#     if request.content_type == "application/json":
#         return jsonify({"message": "Task created successfully", "task_id": new_task.id}), 201
#     else:
#         # Redirect to task list page for browser
#         return redirect(url_for("task_routes.list_tasks"))
    
@task_routes.route("/tasks/create", methods=["GET","POST"])
@login_required
def create_task():
    if request.method == "GET":
        # Show HTML form in browser
        return render_template("task_create.html")
    # data = request.json or request.form
    data = {
            "title": request.form.get("title"),
            "description": request.form.get("description"),
            "status": request.form.get("status"),
            "priority": request.form.get("priority"),
            "due_date": request.form.get("due_date")
        }
    title = data.get('title')
    if not title or len(title) > 200:
        return jsonify({"error": "Title is required (max 200 chars)"}), 400

    due_date_str = data.get('due_date')
    if due_date_str:
        try:
            due_date = datetime.fromisoformat(due_date_str).date()
            if due_date < datetime.utcnow().date():
                return jsonify({"error": "due_date must be today or future"}), 400
        except ValueError:
            return jsonify({"error": "Invalid date format"}), 400
    else:
        due_date = None

    status = data.get('status', 'todo')
    if status not in VALID_STATUS:
        return jsonify({"error": f"status must be one of {VALID_STATUS}"}), 400

    priority = data.get('priority', 'normal')
    if priority not in VALID_PRIORITY:
        return jsonify({"error": f"priority must be one of {VALID_PRIORITY}"}), 400

    task = Task(
        title=title,
        description=data.get('description'),
        due_date=due_date,
        status=status,
        priority=priority,
        owner_id=current_user.id
    )
    db.session.add(task)
    db.session.commit()
    return redirect(url_for("task_routes.list_tasks"))
    # return jsonify(serialize_task(task)), 201

# List Tasks
@task_routes.route("/tasks", methods=["GET"])
@login_required
def list_tasks():
    query = Task.query
    if not current_user.is_admin:
        query = query.filter_by(owner_id=current_user.id)

    # Filters
    status = request.args.get('status')
    priority = request.args.get('priority')
    q = request.args.get('q')
    if status in VALID_STATUS:
        query = query.filter_by(status=status)
    if priority in VALID_PRIORITY:
        query = query.filter_by(priority=priority)
    if q:
        query = query.filter(Task.title.ilike(f"%{q}%"))

    # Pagination
    tasks = paginate(query)
    # Render HTML if browser accepts HTML
    if request.accept_mimetypes.accept_html:
        return render_template("task_list.html", tasks=tasks, current_user=current_user,)
    return jsonify([serialize_task(t) for t in tasks]), 200


# Get Task by ID
@task_routes.route("/tasks/<int:task_id>", methods=["GET"])
@login_required
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner_id != current_user.id and not current_user.is_admin:
        return jsonify({"error": "Forbidden"}), 403
    return jsonify(serialize_task(task)), 200

# Update Task (PATCH)
@task_routes.route("/tasks/<int:task_id>", methods=["PATCH"])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner_id != current_user.id and not current_user.is_admin:
        return jsonify({"error": "Forbidden"}), 403

    data = request.json or {}

    if 'title' in data:
        title = data['title']
        if not title or len(title) > 200:
            return jsonify({"error": "Title must be 1-200 chars"}), 400
        task.title = title

    if 'description' in data:
        task.description = data['description']

    if 'due_date' in data:
        try:
            due_date = datetime.fromisoformat(data['due_date']).date()
            if due_date < datetime.utcnow().date():
                return jsonify({"error": "due_date must be today or future"}), 400
            task.due_date = due_date
        except ValueError:
            return jsonify({"error": "Invalid date format"}), 400

    if 'status' in data:
        if data['status'] not in VALID_STATUS:
            return jsonify({"error": f"status must be one of {VALID_STATUS}"}), 400
        task.status = data['status']

    if 'priority' in data:
        if data['priority'] not in VALID_PRIORITY:
            return jsonify({"error": f"priority must be one of {VALID_PRIORITY}"}), 400
        task.priority = data['priority']

    db.session.commit()
    return jsonify(serialize_task(task)), 200

# Delete Task
@task_routes.route("/tasks/<int:task_id>", methods=["DELETE"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner_id != current_user.id and not current_user.is_admin:
        return jsonify({"error": "Forbidden"}), 403
    db.session.delete(task)
    db.session.commit()
    return '', 204
