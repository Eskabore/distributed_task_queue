import pymongo
from app import app
from flask import request, jsonify, render_template, redirect, url_for, flash
import sys
from app.database import tasks_collection, redis_conn
from rq import Queue
from bson import ObjectId
from datetime import datetime
from app.worker import clean_data, transform_data, analyze_data
from app.task import Task

# Priority mapping for filtering tasks by priority
priority_mapping = {
    "low": 0,
    "medium": 1,
    "high": 2
}

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
    return render_template('index.html')

@app.route('/tasks/create', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        task_data = {
            'description': request.form['description'],
            'priority': request.form['priority'],
            'task_type': request.form['task_type'],
        }
        
        response, status = create_task_with_data(task_data)

        if status == 201:
            task_id = response['task_id']
            flash(f'Task created successfully with ID: {task_id}')
            return redirect(url_for('get_task', task_id=task_id))
        else:
            flash(f'Error creating task: {response["error"]}')
            return render_template('create_task.html'), status
    else:
        return render_template('create_task.html')


# New function to create a task with the given data
def create_task_with_data(data):
    # Validate required fields
    if 'description' not in data or 'priority' not in data or 'task_type' not in data:
        return {'error': 'Missing required fields'}, 400
    
    # Create a Task object
    new_task = Task(data)
    # Save the task to the database
    new_task.save()

    # Add 'created_at' field with the current timestamp as an ISO-formatted string
    data['created_at'] = datetime.utcnow()
    # Add 'status' field with the default value 'pending'
    data['status'] = 'pending'

    allowed_task_types = ['data_cleaning', 'data_transformation', 'data_analysis']

    if data['task_type'] not in allowed_task_types:
        return {'error': 'Invalid task type'}, 400

    task_id = tasks_collection.insert_one(data).inserted_id

    # Determine target queue based on priority
    priority = priority_mapping.get(data['priority'], 1)  # Default to low priority if not provided

    if priority == 'high':
        target_queue = high_priority_queue
    elif priority == 'medium':
        target_queue = medium_priority_queue
    else:
        target_queue = low_priority_queue

    task_type_to_function = {
        'data_cleaning': clean_data,
        'data_transformation': transform_data,
        'data_analysis': analyze_data,
    }

    worker_function = task_type_to_function[data['task_type']]

    job = target_queue.enqueue_call(
    func=task_type_to_function[data['task_type']],
    args=(str(task_id), data),
    result_ttl=86400
)

    return {'task_id': str(task_id)}, 201




# Function to get the status and result of a task
@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    task = tasks_collection.find_one({'_id': ObjectId(task_id)}, sort=[('priority', -1), ('created_at', 1)])
    if not task:
        flash('Task not found')
        return redirect(url_for('index'))

    return render_template('view_task.html', task=task)



# Route for monitoring task status
@app.route('/tasks/<job_id>/status', methods=['GET'])
def get_task_status(job_id):
    job = None
    for queue in [high_priority_queue, medium_priority_queue, low_priority_queue]:
        job = queue.fetch_job(job_id)
        if job:
            break
        
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    task_status = job.get_status()
    return render_template('task_status.html', task_id=job_id, status=task_status, result=job.result if task_status == 'finished' else None)


# Function to update the status of a task
@app.route('/tasks/<task_id>/status', methods=['PUT'])
def update_task_status(task_id):
    if request.content_type != 'application/json':
        return 'request Content-Type was not "application/json".', 415
    
    data = request.get_json()
    new_status = data.get('status', None)
    new_result = data.get('result', None)  # Get the result from the request data
    if new_result:
        update_data['result'] = new_result
        print("New result:", new_result)
    if new_status:
        update_data = {'status': new_status}
        if new_result:
            update_data['result'] = new_result  # Add the result to the update data if it's not None

        tasks_collection.update_one(
            {'_id': ObjectId(task_id)},
            {'$set': update_data}
        )
        return jsonify({'message': 'Task status updated'}), 200
    else:
        return jsonify({'error': 'Invalid status'}), 400

    if new_result:
        update_data['result'] = new_result
        print("New result:", new_result)
    
@app.route('/tasks/<task_id>/details', methods=['GET'])
def get_task_details(task_id):
    task = tasks_collection.find_one({'_id': ObjectId(task_id)})
    if task:
        response = {
            'task_id': str(task['_id']),
            'description': task['description'],
            'priority': task['priority'],
            'created_at': task.get('created_at', None),  # Use get() to avoid KeyError
            'status': task.get('status', None)  # Use get() to avoid KeyError
        }
        return jsonify(response), 200
    else:
        return jsonify({'error': 'Task not found'}), 404



# Function to retrieve all tasks
@app.route('/tasks/view', methods=['GET'])
def get_all_tasks():
    # Get query parameters for pagination, sorting, and filtering
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'asc')
    priority = request.args.get('priority', None)
    status = request.args.get('status', None)
    search = request.args.get('search', None)

    tasks_data = get_all_tasks_data(page, per_page, sort_by, sort_order, priority, status, search)

    # Render the tasks_data and pagination data in the template (adapt this to your needs)
    return render_template('tasks_view.html', tasks=tasks_data['tasks'], pagination=tasks_data['pagination'])


def get_all_tasks_data(page, per_page, sort_by, sort_order, priority, status, search):
    # Build filter query based on priority and status
    filter_query = {}
    if priority:
        filter_query['priority'] = priority_mapping.get(priority)
    if status:
        filter_query['status'] = status
    if search:
        filter_query['description'] = {'$regex': search, '$options': 'i'}

    # Build sort query based on sort_by and sort_order
    sort_query = [(sort_by, pymongo.ASCENDING if sort_order == 'asc' else pymongo.DESCENDING)]

    # Retrieve tasks from collection using find(), skip(), limit(), and sort()
    tasks = tasks_collection.find(filter_query).skip((page - 1) * per_page).limit(per_page).sort(sort_query)

    # Get the total number of tasks
    total_tasks = tasks_collection.count_documents(filter_query)

    # Calculate the total number of pages
    total_pages = total_tasks // per_page + (1 if total_tasks % per_page > 0 else 0)

    # Convert tasks to JSON format
    response = {
        'tasks': [],
        'pagination': {
            'current_page': page,
            'total_pages': total_pages,
            'per_page': per_page
        }
    }
    for task in tasks:
        task_obj = Task(task)
        task_obj.id = str(task['_id'])
        response['tasks'].append({
            'task_id': task_obj.id,
            'description': task_obj.input_data.get('description'),
            'priority': task_obj.input_data.get('priority'),
            'created_at': task_obj.created_at,
            'status': task_obj.status,
            'result': task_obj.result
        })

    return response




# Function to delete a task by ID
@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = tasks_collection.find_one({'_id': ObjectId(task_id)})
    if task:
        tasks_collection.delete_one({'_id': ObjectId(task_id)})

        # Get the job_id from the task document
        job_id = task.get('job_id', None)  # Use get() to avoid KeyError

        # Cancel the corresponding job in the task queue
        if job_id:
            for queue in [low_priority_queue, medium_priority_queue, high_priority_queue]:
                job = queue.fetch_job(job_id)
                if job:
                    job.cancel()
                    break

        return jsonify({'message': 'Task deleted'}), 200
    else:
        return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks/delete_all', methods=['DELETE'])
def delete_all_tasks():
    # Delete all tasks in the database
    result = tasks_collection.delete_many({})

    # Cancel all jobs in the task queues
    for queue in [low_priority_queue, medium_priority_queue, high_priority_queue]:
        job_ids = [job.id for job in queue.get_jobs()]
        for job_id in job_ids:
            job = queue.fetch_job(job_id)
            if job:
                job.cancel()

    return jsonify({'message': f'{result.deleted_count} tasks deleted'}), 200

