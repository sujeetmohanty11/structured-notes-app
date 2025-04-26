from pymongo.mongo_client import MongoClient
import certifi
import os
from dotenv import load_dotenv

load_dotenv()

class MongoConnect:

    def __init__(self):
        self.user = os.getenv("MONGO_USER")
        self.password = os.getenv("MONGO_PASS")
        self.uri = f"mongodb+srv://{self.user}:{self.password}@dev-env.p8v0udo.mongodb.net/?retryWrites=true&w=majority&appName=dev-env"

        # Create a new client and connect to the server
        self.client = MongoClient(self.uri, tlsCAFile=certifi.where())

        # Send a ping to confirm a successful connection
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        self.db = self.client["structured-notes-db"]

        self.users_collection = self.db["users"]
        self.notes_collection = self.db["notes"]
