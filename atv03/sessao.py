import json
from bson.objectid import ObjectId
from db import conectar_mongo, conectar_redis
from usuario import criarUsuario

db = conectar_mongo()
redis = conectar_redis()

colecao_usuario = db.usuario

def login(email, password):
    try:
        registro = colecao_usuario.find_one({"email": email})
        
        if registro["senha"] == password:
            redis.setex(email, 60, registro["nome"])
            return True
        else:
            print("Usuário não encontrado. Senha ou Email incorreta.")
            return False
    except:
        print("Usuário não encontrado. Senha ou Email incorreta.")
        return False
    
def verificarUsuarios():
    usuarios = list(colecao_usuario.find({}))
    
    if(len(usuarios) == 0):
        print("Registre-se para entrar no sistema: ")
        criarUsuario()
        

def verificarSessao(email):
    registro = redis.get(email)
    
    if registro:
        return True  
    else:
        return False 
    
def logout(email):
    redis.delete(email)
    print("Sessão encerrada com sucesso.")
