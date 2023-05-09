import json
from bson import ObjectId
from app import app
from app.database import tasks_collection
import re

def test_index():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert b'Welcome to the Distributed Task Queue' in response.data

def test_create_task():
    app.secret_key = 'testing_key'
    with app.test_client() as client:
        new_task = {
            'description': 'Test task',
            'priority': 'low',
            'task_type': 'data_cleaning'
        }

        response = client.post('/tasks/create', data=new_task)
        assert response.status_code == 302

        # Extract the task ID from the redirection URL
        task_id = re.search(r'/tasks/([\w\d]+)', response.location).group(1)

        # Clean up the test task
        tasks_collection.delete_one({'_id': ObjectId(task_id)})

def test_get_task():
    with app.test_client() as client:
        # Create a test task
        new_task = {
            'description': 'Test task',
            'priority': 'low',
            'task_type': 'data_cleaning'
        }
        task_id = tasks_collection.insert_one(new_task).inserted_id

        # Get the created task
        response = client.get(f'/tasks/{task_id}')
        assert response.status_code == 200
        assert b'Test task' in response.data

        # Clean up the test task
        tasks_collection.delete_one({'_id': ObjectId(task_id)})

def test_get_all_tasks():
    with app.test_client() as client:
        response = client.get('/tasks/view')
        assert response.status_code == 200

def test_search_tasks():
    with app.test_client() as client:
        response = client.get('/tasks/view?search=Test')
        assert response.status_code == 200
        assert b'Test task' in response.data

