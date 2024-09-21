from pymongo.mongo_client import MongoClient 
from datetime import date

uri = "mongodb+srv://friendakouseimanu:asdfg@cluster0.1trpq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo = MongoClient(uri).Rankings
chatdb = mongo.chat


def increase_count(chat, user):
    user = str(user)
    today = str(date.today())
    user_db = chatdb.find_one({"chat": chat})

    if not user_db:
        user_db = {today: {}}
    elif not user_db.get(today):
        user_db[today] = {}

    if user in user_db[today]:
        user_db[today][user] += 1
    else:
        user_db[today][user] = 1

    chatdb.update_one({"chat": chat}, {"$set": {today: user_db[today]}}, upsert=True)

def get_total_users():
    return chatdb.count_documents({})  # Count distinct users in the database

def get_total_chats():
    return chatdb.count_documents({})  # Count total chat documents (you may need to adjust this if you track chats differently)

def get_total_messages():
    total_messages = 0
    for chat in chatdb.find():
        for day_data in chat.values():
            if isinstance(day_data, dict):
                total_messages += sum(day_data.values())
    return total_messages

name_cache = {}

async def get_name(app, id):
    global name_cache

    if id in name_cache:
        return name_cache[id]
    else:
        try:
            i = await app.get_users(id)
            i = f'{(i.first_name or "")} {(i.last_name or "")}'
            name_cache[id] = i
            return i
        except:
            return id
