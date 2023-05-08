from app.task import update_task_status

def clean_data(task_id, input_data):
    # Update the task status to "in progress"
    update_task_status(task_id, "in progress")

    try:
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

    except Exception as e:
        # Update the task status to "failed" if there's an error
        update_task_status(task_id, "failed")
        raise e

    return cleaned_data

def transform_data(task_id, task_data):
    # Update the task status to "in progress"
    update_task_status(task_id, "in progress")
    
    try:
        # Perform data transformation
        transformed_data = task_data.upper()

        # Update the task status in the database
        update_task_status(task_id, "completed")

    except Exception as e:
        # Update the task status to "failed" if there's an error
        update_task_status(task_id, "failed")
        raise e

    return transformed_data


def analyze_data(task_id, task_data):
     # Update the task status to "in progress"
    update_task_status(task_id, "in progress")
    
    try:
        # Perform data analysis
        analysis_result = len(task_data.split())

        # Update the task status in the database
        update_task_status(task_id, "completed")

    except Exception as e:
        # Update the task status to "failed" if there's an error
        update_task_status(task_id, "failed")
        raise e

    return analysis_result


    
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

"""
# Function stimulates task processing and update task status in MongoDB
def perform_task(task_id, data, task_type):
    # Map task_type to worker functions
    task_type_to_function = {
        'data_cleaning': clean_data,
        'data_transformation': transform_data,
        'data_analysis': analyze_data,
    }

    # Get the worker function based on the task_type
    worker_function = task_type_to_function.get(task_type)

    # Call the worker function with task_id and data as arguments
    result = worker_function(task_id, data)

    # Update task status and result in MongoDB
    tasks_collection.find_one_and_update(
        {'_id': MongoClient().task_queue.tasks_collection.ObjectId(task_id)},
        {'$set': {'status': 'completed', 'result': result}},
        return_document=ReturnDocument.AFTER
    )
"""