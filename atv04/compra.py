from bson import ObjectId
from db import conectar_mongo
from produto import mostrarTodosProdutos
from usuario import mostrarTodosUsuarios

db = conectar_mongo()

colecao_compra = db.compra
colecao_usuario = db.usuario
colecao_produto = db.produto

def mostrarTodasCompras():
    print("\nListagem de Compras")
    compras = list(colecao_compra.find({}))

    for index, compra in enumerate(compras):
        print(f'{index} - {compra["usuario"]["nome"]} - {compra["data"]}: R${compra["valor"]}')

def listarCompraDict(compra_dict):
    for key in compra_dict:
        if key == "produtos": 
            print("-- Produtos: ")
            for item_compra in compra_dict["produtos"]:
                print(f"> {item_compra['produto']['nome']} | Quantidade: {item_compra['quantidade']} | Subtotal: {item_compra['subtotal']}")
            continue
        if key == "usuario":
            print(f'{key}: {compra_dict[key]["nome"]}')
            continue
        print(f'{key}: {compra_dict[key]}')

def criarCompra():
    print("\n======== Inserindo uma nova compra ========")

    data = input("Data: ")

    print("Escolha os produtos e sua quantidade: ")
    itens = []

    while True:
        mostrarTodosProdutos()

        opcao_produto = int(input("Index da opção escolhida: "))
        produtos = list(colecao_produto.find({}))

        try:
            produto_escolhido = produtos[opcao_produto]
        except IndexError:
            print("Índice não encontrado! Por favor, escolha um índice válido.")
            return
        
        while True:
            quantidade = int(input(f"Quantidade (disponível: {produto_escolhido['quantidade']}): "))

            if quantidade > int(produto_escolhido['quantidade']): 
                print(f"Quantidade indisponível.")
            else:
                break
            
        item_compra = {
            "produto": produto_escolhido,
            "quantidade": quantidade,
            "subtotal": float(int(produto_escolhido['preco']) * quantidade)
        }

        itens.append(item_compra)
        
        escolha = input("Deseja adicionar mais produtos? [S/N] ")
        if escolha.lower() in ['n', 'nao', 'não']: 
            break

    print('Associe essa compra a um usuário: ')
    mostrarTodosUsuarios()

    usuario_opcao = int(input("Index da opção escolhida: "))
    usuarios = list(colecao_usuario.find({}))

    try:
        usuario_escolhido = usuarios[usuario_opcao]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return
    
    total_sugerido = 0
    for item in itens:
        total_sugerido += item['subtotal']

    valor = float(input(f"Valor total (calculado: {total_sugerido}): "))
    
    compra = {
        "data": data,
        "valor": valor,
        "produtos": itens,
        "usuario": usuario_escolhido
    }

    doc = colecao_compra.insert_one(compra)
    print("Documento inserido com ID ", doc.inserted_id)
 
    for item in itens:
        query_filter = {'_id': ObjectId(item['produto']['_id'])}
        update_operation = { '$set' : {'quantidade': int(item['produto']['quantidade']) - int(item['quantidade'])} }

        result = colecao_produto.update_one(query_filter, update_operation)
        if result.modified_count > 0:
            print(f"Quantidade do produto {item['produto']['nome']} atualizada com sucesso!")
        else:
            print("Nenhuma alteração realizada. Verifique o ID ou os dados.")

def deletarCompra():
    print("\n======== Remover uma Compra ========")

    mostrarTodasCompras()

    opcao = int(input("Index da opção escolhida: "))

    compras = list(colecao_compra.find({}))
    try:
        compras_escolhida = compras[opcao]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return

    query_filter = {'_id': ObjectId(compras_escolhida['_id'])}

    result = colecao_compra.delete_one(query_filter)

    if result.deleted_count > 0:
        print("Compra deletada com sucesso!")
    else:
        print("Nenhuma alteração realizada. Verifique o ID.")
