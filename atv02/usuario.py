from bson import ObjectId
from db import conectar_mongo

db = conectar_mongo()

colecao_usuario = db.usuario

def mostrarTodosUsuarios():
    print("\nListagem de usuário")
    usuarios = list(colecao_usuario.find({}))

    for index, usuario in enumerate(usuarios):
        print(f"{index} - {usuario['nome']}")

def listarUsuarioDict(usuario_dict):
    for key in usuario_dict:
        if(key == "endereco"): 
            print(f'{key}: {usuario_dict[key]["rua"]}, {usuario_dict[key]["bairro"]}, {usuario_dict[key]["cidade"]}, {usuario_dict[key]["estado"]}, {usuario_dict[key]["cep"]}')
            continue
        print(f'{key}: {usuario_dict[key]}')

def criarUsuario():
    print("\n======== Inserindo um novo usuário ========")

    nome = input("Nome: ")
    dataNas = input("Data de Nascimento: ")
    telefone = input("Telefone: ")
    email = input("Email: ")
    senha = input("Senha: ")

    rua = input("Rua: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    estado = input("Estado: ")
    cep = input("Cep: ")

    usuario = {
        "nome": nome,
        "dataNascimento": dataNas,
        "telefone": telefone,
        "email": email,
        "senha": senha,
        "endereco": {
            "rua": rua,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,
            "cep": cep
        }
    }

    doc = colecao_usuario.insert_one(usuario)
    print("Documento inserido com ID ",doc.inserted_id)

def editarUsuario():
    print("\n======== Editar um usuário ========")

    mostrarTodosUsuarios()

    opcao = int(input("Index da opção escolhida: "))

    usuarios = list(colecao_usuario.find({}))
    try:
        usuario_escolhido = usuarios[opcao]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return

    query_filter = {'_id': ObjectId(usuario_escolhido['_id'])}

    nome = input("Nome: ")
    dataNas = input("Data de Nascimento: ")
    telefone = input("Telefone: ")
    email = input("Email: ")
    senha = input("Senha: ")

    rua = input("Rua: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    estado = input("Estado: ")
    cep = input("Cep: ")

    usuario = {
        "nome": nome,
        "dataNascimento": dataNas,
        "telefone": telefone,
        "email": email,
        "senha": senha,
        "endereco": {
            "rua": rua,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,
            "cep": cep
        }
    }

    update_operation = { '$set' : usuario }

    result = colecao_usuario.update_one(query_filter, update_operation)

    if result.modified_count > 0:
        print("Usuário atualizado com sucesso!")
    else:
        print("Nenhuma alteração realizada. Verifique o ID ou os dados.")

def deletarUsuario():
    print("\n======== Remover um usuário ========")

    mostrarTodosUsuarios()

    opcao = int(input("Index da opção escolhida: "))

    usuarios = list(colecao_usuario.find({}))
    try:
        usuario_escolhido = usuarios[opcao]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return

    query_filter = {'_id': ObjectId(usuario_escolhido['_id'])}

    result = colecao_usuario.delete_one(query_filter)

    if result.deleted_count > 0:
        print("Usuário deletado com sucesso!")
    else:
        print("Nenhuma alteração realizada. Verifique o ID.")

def listarUsuario():
    print("\n======== Listar um usuário ========")

    mostrarTodosUsuarios()

    opcao = int(input("Index da opção escolhida: "))

    usuarios = list(colecao_usuario.find({}))
    try:
        usuario_escolhido = usuarios[opcao]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return

    query_filter = {'_id': ObjectId(usuario_escolhido['_id'])}

    result = colecao_usuario.find_one(query_filter)

    listarUsuarioDict(result)


def listarTodosUsuarios():
    print("\n======== Listar todos usuários ========")
    usuarios = list(colecao_usuario.find({}))
    
    for usuario in usuarios:
        print("------------------------------------------------------")
        listarUsuarioDict(usuario)