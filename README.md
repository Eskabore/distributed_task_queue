# Distributed Task Queue

The Distributed Task Queue is a web application that allows users to create tasks and process them asynchronously with prioritization. The application uses Flask, MongoDB, and Redis to efficiently distribute the tasks to workers, which execute them based on their priority.

## Features

- Task creation with priority (low, medium, or high)
- Asynchronous task processing using workers
- Task monitoring and status updates
- Priority-based task processing
- Pagination, sorting, and filtering tasks

## Technologies

- Flask: A lightweight web framework for Python, used to create the web application.
- MongoDB: A NoSQL database used to store tasks.
- Redis: An in-memory data store used as a message broker for the task queue.
- RQ (Redis Queue): A simple Python library for queueing jobs and processing them in the background with workers, built on top of Redis.
- Flask-PyMongo: A Flask extension that provides integration with MongoDB.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/eskabore/distributed_task_queue.git
```


2. Change to the project directory:
```bash
cd distributed_task_queue
```


3. Create a virtual environment:
```bash
python -m venv venv
```


4. Activate the virtual environment:
- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```

5. Install the required packages:
```bash
pip install -r requirements.txt
```


6. Set the Flask environment variables:
- On Windows:
  ```cmd
  set FLASK_APP=app
  set FLASK_ENV=development
  ```
- On macOS and Linux:
  ```bash
  export FLASK_APP=app
  export FLASK_ENV=development
  ```

7. Start the development server:
```bash
flask run
```

8. Open your browser and navigate to `http://localhost:5000/`.

## Usage

1. Create a new task by clicking on "Create Task" and filling out the form.
2. Monitor the status of your tasks by clicking on "View Tasks".
3. View the details of a specific task by clicking on the task ID.

## License

This project is licensed under the **MIT License**.
