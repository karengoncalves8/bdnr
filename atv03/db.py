from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import redis

uri = "mongodb+srv://root:root@cluster0.q4dor.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server MONGODB
def conectar_mongo():
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client.MercadoLivre
    return db

def conectar_redis():
    client = redis.Redis(host='redis-18720.c308.sa-east-1-1.ec2.redns.redis-cloud.com', port=18720, password='2xJNxR9w0qUVEOCxNZygsSSMBq3w1rWi')
    return client