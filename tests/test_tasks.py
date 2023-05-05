import json
from bson import ObjectId
from app import app
from app.database import tasks_collection

def test_index():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert response.data == b'Welcome to the Distributed Task Queue API!'

def test_create_task():
    with app.test_client() as client:
        new_task = {
            'description': 'Test task',
            'priority': 'low',
            'task_type': 'data_cleaning'
        }

        response = client.post('/tasks', json=new_task)
        assert response.status_code == 201
        assert 'task_id' in json.loads(response.data)

        task_id = json.loads(response.data)['task_id']
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
        assert json.loads(response.data)['description'] == 'Test task'

        # Clean up the test task
        tasks_collection.delete_one({'_id': ObjectId(task_id)})

