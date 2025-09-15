import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGODB_URI)
db = client["chatbotDB"]
messages_col = db["messages"]