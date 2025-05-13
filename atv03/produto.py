import json
from bson.objectid import ObjectId
from db import conectar_mongo, conectar_redis
from vendedor import mostrarTodosVendedores

db = conectar_mongo()
redis = conectar_redis()

colecao_produto = db.produto
colecao_vendedor = db.vendedor
colecao_favorito = db.favoritos

def mostrarTodosProdutos():
    print("\nListagem de Produtos")
    produtos = list(colecao_produto.find({}))

    for index, produto in enumerate(produtos):
        print(f'{index} - {produto['nome']}')

def listarProdutoDict(produto_dict):
    for key in produto_dict:
        if(key == "vendedor"): 
            print("-- Informações do vendedor: ")
            for vendedor_key in produto_dict["vendedor"]:
                if(vendedor_key == "endereco"): 
                    print(f"{vendedor_key}: {produto_dict["vendedor"][vendedor_key]["rua"]}, {produto_dict["vendedor"][vendedor_key]["bairro"]}, {produto_dict["vendedor"][vendedor_key]["cidade"]}, {produto_dict["vendedor"][vendedor_key]["estado"]}, {produto_dict["vendedor"][vendedor_key]["cep"]}")
                    continue
                print(f'{vendedor_key}: {produto_dict["vendedor"][vendedor_key]}')
            continue
        print(f'{key}: {produto_dict[key]}')

def criarProduto():
    print("\n======== Inserindo um novo produto ========")

    nome = input("Nome: ")
    preco = float(input("Preço: "))
    quantidade = int(input("Quantidade: "))
    marca = input("Marca: ")
    material = input("Material: ")
    descricao = input("Descrição: ")

    print("Associe a um vendedor: ")

    mostrarTodosVendedores()

    opcao_vendedor = int(input("Index da opção escolhida: "))
    vendedores = list(colecao_vendedor.find({}))

    try:
        vendedor_escolhido = vendedores[opcao_vendedor]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return

    produto = {
        "nome": nome,
        "preco": preco,
        "quantidade": quantidade,
        "marca": marca,
        "material": material,
        "descricao": descricao,
        "vendedor": vendedor_escolhido
    }

    doc = colecao_produto.insert_one(produto)
    print("Documento inserido com ID ",doc.inserted_id)

def editarProduto():
    print("\n======== Editar um produto ========")

    mostrarTodosProdutos()

    opcao = int(input("Index da opção escolhida: "))

    produtos = list(colecao_produto.find({}))
    try:
        produto_escolhido = produtos[opcao]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return
    
    colecao_produto.delete_one(produto_escolhido)

    query_filter = {'_id': ObjectId(produto_escolhido['_id'])}
    
    nome = input("Nome: ")
    preco = input("Preço: ")
    if preco.strip():  
        preco = float(preco)  
    quantidade = input("Quantidade: ")
    if quantidade.strip():  
        quantidade = int(quantidade) 
    marca = input("Marca: ")
    material = input("Material: ")
    descricao = input("Descrição: ")

    print("Associe a um vendedor: ")

    mostrarTodosVendedores()

    opcao_vendedor = int(input("Index da opção escolhida: "))
    vendedores = list(colecao_vendedor.find({}))

    try:
        vendedor_escolhido = vendedores[opcao_vendedor]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return

    produto = {
        "nome": nome if nome else produto_escolhido["nome"],
        "preco": preco if preco else produto_escolhido["preco"],
        "quantidade": quantidade if quantidade else produto_escolhido["quantidade"],
        "marca": marca if marca else produto_escolhido["marca"],
        "material": material if material else produto_escolhido["material"],
        "descricao": descricao if descricao else produto_escolhido["descricao"],
        "vendedor": vendedor_escolhido
    }
    
    redis.set(produto_escolhido['_id'], produto)
    
    produto_atualizado = redis.get(produto_escolhido['_id'])

    query_filter = {'_id': produto_escolhido['_id']}
    update_operation = {'$set': produto_atualizado}

    result = colecao_produto.update_one(query_filter, update_operation)

    if result.modified_count > 0:
        print("Produto atualizado com sucesso!")
    else:
        print("Nenhuma alteração realizada. Verifique o ID ou os dados.")

def deletarProduto():
    print("\n======== Remover um Produto ========")

    mostrarTodosProdutos()

    opcao = int(input("Index da opção escolhida: "))

    produtos = list(colecao_produto.find({}))
    try:
        produto_escolhido = produtos[opcao]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return

    query_filter = {'_id': ObjectId(produto_escolhido['_id'])}

    result = colecao_produto.delete_one(query_filter)

    if result.deleted_count > 0:
        print("Produto deletado com sucesso!")
        
        # Excluir produto dos favoritos
        query_filter = {'produto._id': produto_escolhido['_id']}
        deleted_fav = colecao_favorito.delete_many(query_filter)

        if deleted_fav.deleted_count > 0:
            print("Favoritos removidos com sucesso!")
    else:
        print("Nenhuma alteração realizada. Verifique o ID.")

def listarProduto():
    print("\n======== Listar um produto ========")

    mostrarTodosProdutos()

    opcao = int(input("Index da opção escolhida: "))

    produtos = list(colecao_produto.find({}))
    try:
        produto_escolhido = produtos[opcao]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return

    query_filter = {'_id': ObjectId(produto_escolhido['_id'])}

    result = colecao_produto.find_one(query_filter)

    listarProdutoDict(result)


def listarTodosProdutos():
    print("\n======== Listar todos produtos ========")
    produtos = list(colecao_produto.find({}))
    
    for produto in produtos:
        print("------------------------------------------------------")
        listarProdutoDict(produto)

