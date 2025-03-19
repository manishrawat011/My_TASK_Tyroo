# main.py (Flask example)
from flask import Flask, request, jsonify, g, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import jwt
import logging
import os
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

# App Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///./tasks.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "your_secret_key") # Change in production
db = SQLAlchemy(app)

# JWT Configuration
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Logging Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Models
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), index=True)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

with app.app_context():
    db.create_all()

# JWT Helper Functions
def create_access_token(user_id):
    payload = {
        'exp': datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        'iat': datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm=ALGORITHM)

def decode_access_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=[ALGORITHM])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            token = token.split(" ")[1] #Extract token from "Bearer <token>"
        except:
            return jsonify({'message': 'Invalid Token'}), 401

        user_id = decode_access_token(token)
        if not user_id:
            return jsonify({'message': 'Invalid token'}), 401
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 401

        g.current_user = user
        return f(*args, **kwargs)
    return decorated

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    print(username,password)

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.verify_password(password):
        return jsonify({'message': 'Invalid username or password'}), 401

    access_token = create_access_token(user.id)
    return jsonify({'access_token': access_token}), 200

@app.route('/tasks', methods=['POST'])
@token_required
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if not title:
        return jsonify({'message': 'Title is required'}), 400

    new_task = Task(title=title, description=description, user_id=g.current_user.id)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'message': 'Task created successfully'}), 201

@app.route('/tasks', methods=['GET'])
@token_required
def get_tasks():
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)  # Get page number (default 1)
    per_page = request.args.get('per_page', 10, type=int)  # Get items per page (default 10)

    query = Task.query.filter_by(user_id=g.current_user.id)
    if status:
        query = query.filter_by(status=status)

    paginated_tasks = query.paginate(page=page, per_page=per_page)
    tasks = [{'id': task.id, 'title': task.title, 'description': task.description, 'status': task.status, 'created_at': task.created_at, 'updated_at': task.updated_at} for task in paginated_tasks.items]

    # Include pagination metadata in the response
    pagination_info = {
        'total_pages': paginated_tasks.pages,
        'current_page': paginated_tasks.page,
        'per_page': paginated_tasks.per_page,
        'total_items': paginated_tasks.total,
    }

    return jsonify({'tasks': tasks, 'pagination': pagination_info}), 200
# def get_tasks():
#     status = request.args.get('status')
#     page = request.args.get('page', 1, type=int)
#     per_page = request.args.get('per_page', 10, type=int)
#
#     query = Task.query.filter_by(user_id=g.current_user.id)
#     if status:
#         query = query.filter_by(status=status)
#
#     paginated_tasks = query.paginate(page=page, per_page=per_page)
#     tasks = [{'id': task.id, 'title': task.title, 'description': task.description, 'status': task.status, 'created_at': task.created_at, 'updated_at': task.updated_at} for task in paginated_tasks.items]
#     return jsonify(tasks), 200

@app.route('/tasks/<int:task_id>', methods=['GET'])
@token_required
def get_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=g.current_user.id).first()
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    return jsonify({'id': task.id, 'title': task.title, 'description': task.description, 'status': task.status, 'created_at': task.created_at, 'updated_at': task.updated_at}), 200

@app.route('/tasks/<int:task_id>', methods=['PUT'])
@token_required
def update_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=g.current_user.id).first()
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    db.session.commit()
    return jsonify({'message': 'Task updated successfully'}), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=g.current_user.id).first()
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200


if __name__ == '__main__':
    app.run(port=5000)