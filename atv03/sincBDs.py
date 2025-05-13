import json
from bson.objectid import ObjectId
from db import conectar_mongo, conectar_redis

db = conectar_mongo()
redis = conectar_redis()

colecao_compra = db.compra

def sinc_bds():
    compras_deletadas = 0
    compras_atualizadas = 0
    
    for key in redis.scan_iter("*"):
        key_str = key.decode()
        if '@' not in key_str:  
            query_filter = {'_id': ObjectId(key_str)}

            try:
                result = colecao_compra.find_one(query_filter)
            except:
                print(f"Erro! Registro de compra de id: {key_str} não encontrado no MongoDB.")
                return
            
            value = redis.get(key_str)  
        
            print("value", value)
            
            if isinstance(value, bytes):
                print("decodigicando")
                value = value.decode('utf-8') 
            
            if value == 'deleted': 
                print("deleting")
                result = colecao_compra.delete_one(query_filter)

                if result.deleted_count > 0:
                    compras_deletadas += 1
                else:
                    print("Nenhuma alteração realizada. Verifique o ID.")
            else:
                compra_atualizada = json.loads(value)

                compra_com_objectids = convert_str_to_objectid(compra_atualizada)
                update_operation = {'$set': compra_com_objectids}

                result = colecao_compra.update_one(query_filter, update_operation)
                
                if result.modified_count > 0:
                    compras_atualizadas += 1
                else:
                    print("Nenhuma alteração realizada. Verifique o ID ou os dados.")
            redis.delete(key_str)
            
    print(f"Mongo DB atualizado! {compras_atualizadas} compras atualizadas e {compras_deletadas} deletadas")
                
def convert_str_to_objectid(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == '_id' and isinstance(value, str):
                obj[key] = ObjectId(value)
            else:
                convert_str_to_objectid(value)
    elif isinstance(obj, list):
        for item in obj:
            convert_str_to_objectid(item)
    return obj

            