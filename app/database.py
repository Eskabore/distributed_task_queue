import os
import sys
from dotenv import load_dotenv
from redis import Redis
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from app import app

# Load environment variables from .env file
dotenv_path = "/mnt/f/CS50P/finalproject/distributed_task_queue/venv/.env"
load_dotenv(dotenv_path)

# Get the username and password from the environment variables
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# Redis connection
redis_conn = Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'])
print(redis_conn.ping())

# Check Redis connection
try:
    redis_conn.ping()
    print("Successfully connected to Redis.")
except Exception as e:
    print("Error connecting to Redis: ", e, file=sys.stderr)
    sys.exit(1)

# MongoDB connection
host = "localhost" or "127.0.0.1"
port = "27017" or "27018" or "27019"
database_name = "distributed_task_queues" or "task_queue"

uri = f"mongodb+srv://{username}:{password}@cluster0.tjer16g.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
#print(client.server_info())
db = client[database_name]
tasks_collection = db['tasks']
