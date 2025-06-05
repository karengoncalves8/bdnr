import time
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
    while True:
        try:
            cliente_redis = redis.StrictRedis(
                host='redis-14368.c14.us-east-1-2.ec2.redns.redis-cloud.com',
                port=14368,
                password='Y3uUgk7lzkQbf7onGmrWiSFkZQWQZ8Jl',
                db=0,
                socket_timeout=5  
            )
            cliente_redis.ping()  
            print("Conectado ao Redis com sucesso!")
            return cliente_redis 
        except redis.ConnectionError as e:
            print(f"Erro ao conectar ao Redis: {e}. Tentando novamente em 5 segundos...")
            time.sleep(5)  