from bson import ObjectId
from db import conectar_mongo

db = conectar_mongo()

colecao_vendedor = db.vendedor
vendedores = list(colecao_vendedor.find({}))

def mostrarTodosVendedores():
    print("\nListagem de vendedores")

    for index, vendedor in enumerate(vendedores):
        print(f'{index} - {vendedor['nome']}')

def listarVendedorDict(vendedor_dict):
    for key in vendedor_dict:
        if(key == "endereco"): 
            print(f"{key}: {vendedor_dict[key]["rua"]}, {vendedor_dict[key]["bairro"]}, {vendedor_dict[key]["cidade"]}, {vendedor_dict[key]["estado"]}, {vendedor_dict[key]["cep"]}")
            continue
        print(f'{key}: {vendedor_dict[key]}')

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

def editarVendedor():
    print("\n======== Editar um vendedor ========")

    mostrarTodosVendedores()

    opcao = int(input("Index da opção escolhida: "))

    vendedor_escolhido = vendedores[opcao]

    query_filter = {'_id': ObjectId(vendedor_escolhido['_id'])}

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

    update_operation = { '$set' : vendedor }

    result = colecao_vendedor.update_one(query_filter, update_operation)

    if result.modified_count > 0:
        print("Vendedor atualizado com sucesso!")
    else:
        print("Nenhuma alteração realizada. Verifique o ID ou os dados.")

def deletarVendedor():
    print("\n======== Remover um vendedor ========")

    mostrarTodosVendedores()

    opcao = int(input("Index da opção escolhida: "))

    vendedor_escolhido = vendedores[opcao]

    query_filter = {'_id': ObjectId(vendedor_escolhido['_id'])}

    result = colecao_vendedor.delete_one(query_filter)

    if result.deleted_count > 0:
        print("Vendedor deletado com sucesso!")
    else:
        print("Nenhuma alteração realizada. Verifique o ID.")

def listarVendedor():
    print("\n======== Listar um vendedor ========")

    mostrarTodosVendedores()

    opcao = int(input("Index da opção escolhida: "))

    vendedor_escolhido = vendedores[opcao]

    query_filter = {'_id': ObjectId(vendedor_escolhido['_id'])}

    result = colecao_vendedor.find_one(query_filter)

    listarVendedorDict(result)


def listarTodosVendedores():
    print("\n======== Listar todos vendedores ========")
    for vendedor in vendedores:
        print("------------------------------------------------------")
        listarVendedorDict(vendedor)

