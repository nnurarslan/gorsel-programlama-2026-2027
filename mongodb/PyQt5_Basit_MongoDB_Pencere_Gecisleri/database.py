from pymongo import MongoClient

# MongoDB Community Server bilgisayarda çalışıyor olmalı.
client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
db = client["gorsel_programlama_db"]
users = db["kullanicilar"]


def check_connection():
    client.admin.command("ping")
    users.create_index("email", unique=True)
