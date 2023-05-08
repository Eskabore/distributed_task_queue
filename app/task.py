# Description: This file contains the task related functions
from bson.objectid import ObjectId
from app.database import tasks_collection
from datetime import datetime

def update_task_status(task_id, status):
    # Update the task status based on the given task_id
    tasks_collection.update_one(
        {"_id": ObjectId(task_id)},  # Query to find the task with the given task_id
        {"$set": {"status": status}}  # Update operation to set the new status
    )

    print(f"Task {task_id} updated to status: {status}")

class Task:
    def __init__(self, input_data):
        self.input_data = input_data
        self.status = "pending"
        self.result = None
        self.created_at = datetime.now()

    def save(self):
        task_data = {
            "input_data": self.input_data,
            "status": self.status,
            "result": self.result,
            "created_at": self.created_at
        }
        result = tasks_collection.insert_one(task_data)
        self.id = str(result.inserted_id)

    def update_status(self):
        update_task_status(self.id, self.status)
