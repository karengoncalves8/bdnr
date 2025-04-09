from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://root:root@cluster0.q4dor.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
def conectar_mongo():
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client.MercadoLivre
    return db

