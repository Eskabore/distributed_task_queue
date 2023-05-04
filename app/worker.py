import time
import random
from app.database import tasks_collection
from pymongo import MongoClient, ReturnDocument

# Function stimulates task processing and update task status in MongoDB
def perform_task(task_id, data):
    # Simulate task processing time
    processing_time = random.randint(1, 10)
    time.sleep(processing_time)

    # Update task status and result in MongoDB
    result = "Task completed in {} seconds.".format(processing_time)
    tasks_collection.find_one_and_update(
        {'_id': MongoClient().task_queue.tasks_collection.ObjectId(task_id)},
        {'$set': {'status': 'completed', 'result': result}},
        return_document=ReturnDocument.AFTER
    )
    
"""
# Function stimulates task processing and update task status in MongoDB
def perform_task(task_id, data):
    # Get the task description and priority from the data
    description = data.get('description', None)
    priority = data.get('priority', 'low')

    # Perform different actions based on the task description and priority
    if description == 'Send an email':
        # Call an external API to send an email
        result = send_email(data)
    elif description == 'Process data':
        # Process some data using a custom function
        result = process_data(data)
    elif description == 'Perform other action':
        # Perform some other action based on the priority
        if priority == 'high':
            result = do_something_urgent(data)
        elif priority == 'medium':
            result = do_something_important(data)
        else:
            result = do_something_normal(data)
    else:
        # Default action if no description is given
        result = do_something_default(data)

    # Update task status and result in MongoDB
    tasks_collection.find_one_and_update(
        {'_id': MongoClient().task_queue.tasks_collection.ObjectId(task_id)},
        {'$set': {'status': 'completed', 'result': result}},
        return_document=ReturnDocument.AFTER
    )
"""