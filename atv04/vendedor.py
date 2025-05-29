from bson import ObjectId
from db import conectar_mongo

db = conectar_mongo()

colecao_vendedor = db.vendedor
colecao_produto = db.produto

def atualizarProduto(vendedor):
    vendedor_att = colecao_vendedor.find_one({'_id': ObjectId(vendedor['_id'])})

    # Atualizar informações do vendedor nos produtos pertencentes ao mesmo
    query_filter_produto = {'vendedor._id': vendedor['_id']}
    update_operation_usuario = { '$set': {'vendedor': vendedor_att}}

    result = colecao_produto.update_many(query_filter_produto, update_operation_usuario)

    if result.modified_count > 0:
        print(f"Produtos do vendedor atualizado com sucesso!")
    else:
        print("Nenhuma alteração nos produtos do vendedor.")

def criarVendedor():
    print("\n======== Inserindo um novo vendedor ========")

    nome = input("Nome: ")
    dataNas = input("Data de Nascimento: ")
    telefone = input("Telefone: ")
    email = input("Email: ")
    senha = input("Senha: ")
    cnpj = input("CNPJ: ")

    rua = input("Rua: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    estado = input("Estado: ")
    cep = input("Cep: ")

    vendedor = {
        "nome": nome,
        "dataNascimento": dataNas,
        "telefone": telefone,
        "email": email,
        "senha": senha,
        "cnpj": cnpj,
        "endereco": {
            "rua": rua,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,
            "cep": cep
        }
    }

    doc = colecao_vendedor.insert_one(vendedor)
    print("Documento inserido com ID ",doc.inserted_id)