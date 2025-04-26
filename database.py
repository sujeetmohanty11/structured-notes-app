from pymongo.mongo_client import MongoClient
import certifi
import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASS")
uri = f"mongodb+srv://{user}:{password}@dev-env.p8v0udo.mongodb.net/?retryWrites=true&w=majority&appName=dev-env"

# Create a new client and connect to the server
client = MongoClient(uri, tlsCAFile=certifi.where())

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["structured-notes-db"]

users_collection = db["users"]
notes_collection = db["notes"]
