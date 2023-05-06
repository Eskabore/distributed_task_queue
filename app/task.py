# Description: This file contains the task related functions
from bson.objectid import ObjectId
from app.database import tasks_collection


def update_task_status(task_id, status):
    # Update the task status based on the given task_id
    tasks_collection.update_one(
        {"_id": ObjectId(task_id)},  # Query to find the task with the given task_id
        {"$set": {"status": status}}  # Update operation to set the new status
    )

    print(f"Task {task_id} updated to status: {status}")
