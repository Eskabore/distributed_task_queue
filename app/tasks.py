from app import app
from flask import request, jsonify
import sys
from app.database import tasks_collection, redis_conn
from app.worker import perform_task
from rq import Queue
from bson import ObjectId


# RQ queues
low_priority_queue = Queue('low', connection=redis_conn)
medium_priority_queue = Queue('medium', connection=redis_conn)
high_priority_queue = Queue('high', connection=redis_conn)

# Check RQ queue connection
try:
    queue_length = low_priority_queue.count  # Updated to use low_priority_queue instead of queue
    print(f"Successfully connected to RQ queue. Current queue length: {queue_length}")
except Exception as e:
    print("Error connecting to RQ queue: ", e, file=sys.stderr)
    sys.exit(1)

@app.route('/', methods=['GET'])
def index():
    return "Welcome to the Distributed Task Queue API!"

# Function to create a new task
@app.route('/tasks', methods=['POST'], content_type="application/json")
def create_task():
    data = request.get_json()
    task_id = tasks_collection.insert_one(data).inserted_id

    # Determine target queue based on priority
    priority = data.get('priority', 'low')
    if priority == 'high':
        target_queue = high_priority_queue
    elif priority == 'medium':
        target_queue = medium_priority_queue
    else:
        target_queue = low_priority_queue

    job = target_queue.enqueue_call(
        perform_task,
        args=(str(task_id), data),
        result_ttl=86400
    )
    return jsonify({'task_id': str(task_id), 'job_id': job.id}), 201

# Function to get the status and result of a task
@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    task = tasks_collection.find_one({'_id': ObjectId(task_id)})
    if task:
        response = {
            'task_id': str(task['_id']),
            'status': task['status'],
            'result': task.get('result', None)
        }
        return jsonify(response)
    else:
        return jsonify({'error': 'Task not found'}), 404
