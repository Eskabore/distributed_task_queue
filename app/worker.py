from app.database import tasks_collection
from pymongo import MongoClient, ReturnDocument

# Function stimulates task processing and update task status in MongoDB
def perform_task(worker_function, task_id, data):
    # Call the worker function with task_id and data as arguments
    result = worker_function(task_id, data)

    # Update task status and result in MongoDB
    tasks_collection.find_one_and_update(
        {'_id': MongoClient().task_queue.tasks_collection.ObjectId(task_id)},
        {'$set': {'status': 'completed', 'result': result}},
        return_document=ReturnDocument.AFTER
    )
    
def clean_data(task_id, input_data):
    # Perform data cleaning

    # Step 1: Remove leading and trailing whitespaces
    cleaned_data = input_data.strip()

    # Step 2: Replace multiple spaces with a single space
    cleaned_data = ' '.join(cleaned_data.split())

    # Step 3: Convert text to lowercase
    cleaned_data = cleaned_data.lower()

    # Add more data cleaning steps as required

    # Update the task status in the database
    update_task_status(task_id, "completed")

    return cleaned_data


def transform_data(task_id, input_data):
    # Perform data transformation
    ...

def analyze_data(task_id, input_data):
    # Perform data analysis
    ...

    
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