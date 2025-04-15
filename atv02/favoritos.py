from bson import ObjectId
from db import conectar_mongo

from produto import mostrarTodosProdutos
from usuario import mostrarTodosUsuarios

db = conectar_mongo()

colecao_favorito = db.favorito
colecao_produto = db.produto
colecao_usuario = db.usuario

def atualizarUsuarioFavoritos(favorito):
    # Atualizar o favorito na lista de favoritos do usuário
    query_filter_usuario = {'_id': ObjectId(favorito['usuario']['_id'])}

    usuario_favoritos = list(colecao_favorito.find({'usuario._id': favorito['usuario']['_id']}))
    novos_favoritos = [fav['produto'] for fav in usuario_favoritos]

    update_operation_usuario = { '$set': {'favoritos':  novos_favoritos}}

    result_usuario = colecao_usuario.update_one(query_filter_usuario, update_operation_usuario)

    if result_usuario.modified_count > 0:
        print(f"Lista de favoritos do usuário atualizada com sucesso!")
    else:
        print("Nenhuma alteração na lista de favoritos do usuário.")

def mostrarTodosFavoritos():
    print("\nListagem de Favoritos")
    favoritos = list(colecao_favorito.find({}))

    for index, favorito in enumerate(favoritos):
        print(f'{index} - {favorito['produto']['nome']} de {favorito['usuario']['nome']}')

def listarFavoritoDict(favorito_dict):
    for key in favorito_dict:
        if(key == "produto"): 
            print('-- Informações do produto')
            for produto_key in favorito_dict["produto"]:
                if(produto_key == "vendedor"): 
                    print(f"{key}: {favorito_dict[key][produto_key]["nome"]}")
                    continue
                print(f'{produto_key}: {favorito_dict[key][produto_key]}')
            continue
        if(key == "usuario"): 
            print('-- Informações do usuário')
            for usuario_key in favorito_dict["usuario"]:
                if(usuario_key == "favoritos"): break
                print(f'{usuario_key}: {favorito_dict[key][usuario_key]}')
            continue
        print(f'{key}: {favorito_dict[key]}')

def criarFavorito():
    print("\n======== Inserindo um novo favorito ========")

    print("Escolha um produto a ser favoritado:")
    mostrarTodosProdutos()

    opcao_produto = int(input("Index da opção escolhida: "))
    produtos = list(colecao_produto.find({}))

    try:
        produto_escolhido = produtos[opcao_produto]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return

    print("Associe a um usuário: ")

    mostrarTodosUsuarios()

    usuario_opcao = int(input("Index da opção escolhida: "))
    usuarios = list(colecao_usuario.find({}))

    try:
        usuario_escolhido = usuarios[usuario_opcao]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return
    
    favorito = {
        "usuario": usuario_escolhido,
        "produto": produto_escolhido
    }

    doc = colecao_favorito.insert_one(favorito)
    print("Documento inserido com ID ",doc.inserted_id)
    
    # Inserindo favorito ao usuário
    query_filter = {'_id': ObjectId(usuario_escolhido['_id'])}
    update_operation = { '$push': {'favoritos': favorito["produto"]} }

    result = colecao_usuario.update_one(query_filter, update_operation)
    if result.modified_count > 0:
        print(f"Favorito adicionado ao usuário com sucesso!")
    else:
        print("Nenhuma alteração realizada. Verifique o ID ou os dados.")

def editarFavorito():
    print("\n======== Editar um favorito ========")

    mostrarTodosFavoritos()

    opcao = int(input("Index da opção escolhida: "))

    favoritos = list(colecao_favorito.find({}))
    try:
        favorito_escolhido = favoritos[opcao]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return

    query_filter = {'_id': ObjectId(favorito_escolhido['_id'])}
    
    print("Escolha um novo produto para o favorito:")
    mostrarTodosProdutos()

    opcao_produto = int(input("Index da opção escolhida: "))
    produtos = list(colecao_produto.find({}))

    try:
        produto_escolhido = produtos[opcao_produto]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return

    # Atualizar o produto no favorito
    favorito_escolhido['produto'] = produto_escolhido

    print("Associe o favorito a um novo usuário:")
    mostrarTodosUsuarios()

    usuario_opcao = int(input("Index da opção escolhida: "))
    usuarios = list(colecao_usuario.find({}))

    try:
        usuario_escolhido = usuarios[usuario_opcao]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return

    favorito_escolhido['usuario'] = usuario_escolhido

    # Atualizar o favorito na coleção de favoritos
    query_filter = {'_id': ObjectId(favorito_escolhido['_id'])}
    update_operation = { '$set': favorito_escolhido }

    result = colecao_favorito.update_one(query_filter, update_operation)

    if result.modified_count > 0:
        print(f"Favorito atualizado com sucesso!")
    else:
        print("Nenhuma alteração realizada. Verifique o ID ou os dados.")

    atualizarUsuarioFavoritos(favorito_escolhido)

def deletarFavorito():
    print("\n======== Remover um Favorito ========")

    mostrarTodosFavoritos()

    opcao = int(input("Index da opção escolhida: "))

    favoritos = list(colecao_favorito.find({}))
    try:
        favorito_escolhido = favoritos[opcao]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return

    query_filter = {'_id': ObjectId(favorito_escolhido['_id'])}

    result = colecao_favorito.delete_one(query_filter)

    if result.deleted_count > 0:
        print("Favorito deletado com sucesso!")
        atualizarUsuarioFavoritos(favorito_escolhido)
    else:
        print("Nenhuma alteração realizada. Verifique o ID.")

def listarFavorito():
    print("\n======== Listar um favorito ========")

    mostrarTodosFavoritos()

    opcao = int(input("Index da opção escolhida: "))

    favoritos = list(colecao_favorito.find({}))
    try:
        favorito_escolhido = favoritos[opcao]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return

    query_filter = {'_id': ObjectId(favorito_escolhido['_id'])}

    result = colecao_favorito.find_one(query_filter)

    print("\n")
    listarFavoritoDict(result)


def listarTodosFavoritos():
    print("\n======== Listar todos favoritos ========")
    favoritos = list(colecao_favorito.find({}))
    
    for favorito in favoritos:
        print("------------------------------------------------------")
        listarFavoritoDict(favorito)

