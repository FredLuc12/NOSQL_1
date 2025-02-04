from pymongo import MongoClient

import json

import pymongo
from faker import Faker
import faker

client = MongoClient('mongodb://localhost:27017/')

db = client.mydb
collection = db.mycollection


document = {"name": "John Doe", "email": "john.doe@example.com", "age": 30}
result = collection.insert_one(document)
print("Inserted document ID:", result.inserted_id)

documents = [
    {"name": "Alice", "email": "alice@example.com", "age": 25},
    {"name": "Bob", "email": "bob@example.com", "age": 35}
]
result = collection.insert_many(documents)
print("Inserted document IDs:", result.inserted_ids)


query = {"name": "John Doe"}
document = collection.find_one(query)
print(document)


query = {"age": {"$gt": 25}}
documents = collection.find(query)

for doc in documents:
    print(doc)
    

query = {"name": "John Doe"}
update = {"$set": {"age": 31}}
result = collection.update_one(query, update)
print("Modified document count:", result.modified_count)

query = {"age": {"$gt": 25}}
update = {"$inc": {"age": 1}}
result = collection.update_many(query, update)
print("Modified document count:", result.modified_count)


query = {"name": "John Doe"}
result = collection.delete_one(query)
print("Deleted document count:", result.deleted_count)

query = {"age": {"$gt": 25}}
result = collection.delete_many(query)
print("Deleted document count:", result.deleted_count)

query = {
    "$and": [
        {"age": {"$gt": 25}},
        {"email": {"$regex": "@example\.com$"}}
    ]
}
documents = collection.find(query)

for doc in documents:
    print(doc)
    

query = {"age": {"$gt": 25}}
documents = collection.find(query).sort("name", pymongo.ASCENDING)

for doc in documents:
    print(doc)


# Génération de données aléatoires avec Faker
fake = Faker()

accounts = []
for _ in range(10):
    account = {
        "name": fake.name(),
        "email": fake.email(),
        "age": fake.random_int(min=18, max=80),
        "address": {
            "street": fake.street_address(),
            "city": fake.city(),
            "state": fake.state(),
            "zipcode": fake.zipcode()
        },
        "balance": fake.random_int(min=1000, max=50000)
    }
    accounts.append(account)

# Sauvegarder les données dans un fichier JSON
with open("accounts.json", "w") as file:
    json.dump(accounts, file, indent=4)

print("Fichier accounts.json créé avec succès.")

index_name = "city_index"
collection.create_index("address.city", name=index_name)

city = "Bradshawborough"
results = collection.find({"address.city": city})

for result in results:
    print(result)
    

min_balance = 30000
results = collection.find({"balance": {"$gt": min_balance}})

for result in results:
    print(result)
    

pipeline = [
    {"$group": {"_id": "$address.city", "total_balance": {"$sum": "$balance"}}},
    {"$sort": {"total_balance": -1}}
]

results = collection.aggregate(pipeline)

for result in results:
    print(f"{result['_id']}: {result['total_balance']}")
    
# Supprimer les doublons sur le champ "email"
emails_seen = set()
duplicates = collection.find({"email": {"$in": list(emails_seen)}})

for doc in duplicates:
    collection.delete_one({"_id": doc["_id"]})
    emails_seen.add(doc["email"])
    
# Maintenant, tu peux créer l'index unique

index_name = collection.create_index("email")

pipeline = [
    {"$match": {"age": {"$gt": 25}}},
    {"$group": {"_id": "$age", "count": {"$sum": 1}}}
]

results = collection.aggregate(pipeline)

for result in results:
    print(result)
