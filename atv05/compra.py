import uuid
from db import conectar_neo4j
from produto import mostrarTodosProdutos
from usuario import mostrarTodosUsuarios

session = conectar_neo4j()

def criarCompra():
    print("\n======== Inserindo uma nova compra ========")

    data = input("Data: ")

    print("Escolha os produtos e sua quantidade: ")
    itens = []
    produtos_comprados = []

    while True:
        produtos = mostrarTodosProdutos()

        opcao_produto = int(input("Index da opção escolhida: "))

        try:
            produto_escolhido = produtos[opcao_produto]
        except IndexError:
            print("Índice não encontrado! Por favor, escolha um índice válido.")
            return
        
        produto_escolhido = produto_escolhido['p']
        
        while True:
            quantidade = int(input(f"Quantidade (disponível: {produto_escolhido['quantidade']}): "))

            if quantidade > produto_escolhido['quantidade']: 
                print(f"Quantidade indisponível.")
            else:
                break
            
        item_compra = {
            "id": produto_escolhido['id'],
            "quantidade": quantidade,
            "preco": produto_escolhido['preco']
        }

        itens.append(item_compra)
        produtos_comprados.append(produto_escolhido)
        
        escolha = input("Deseja adicionar mais produtos? [S/N] ")
        if escolha.lower() in ['n', 'nao', 'não']: 
            break

    print('Associe essa compra a um usuário: ')
    usuarios = mostrarTodosUsuarios()

    usuario_opcao = int(input("Index da opção escolhida: "))

    try:
        usuario_escolhido = usuarios[usuario_opcao]['u']
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return
    
    total_sugerido = 0
    for item in itens:
        total_sugerido += item['preco'] * item['quantidade']

    valor = float(input(f"Valor total (calculado: {total_sugerido}): "))
    
    compra_id = str(uuid.uuid4())

    query = """
        CREATE (c:Compra {
            id: $id,
            data: $data,
            valor: $valor
        })
        RETURN c.id
    """

    with session.begin_transaction() as tx:
        result = tx.run(query, 
                        id=compra_id,
                        data=data,
                        valor=valor)
        created_id = result.single()[0]

    print(f"Compra criada com sucesso! ID: {created_id}")

    queryRel = """
        MATCH (u:Usuario {id: $usuario_id}), (c:Compra {id: $compra_id})
        MERGE (u)-[:COMPROU]->(c)

        WITH c
        UNWIND $itens AS item  
        MATCH (p:Produto {id: item.id_produto})
        MERGE (c)-[:CONTEM {quantidade: item.quantidade, subtotal: item.subtotal}]->(p)
    """

    with session.begin_transaction() as tx:
        result_rel = tx.run(queryRel, 
                        usuario_id=usuario_escolhido["id"], 
                        compra_id=compra_id, 
                        itens=[{
                            'id_produto': item['id'],
                            'quantidade': item['quantidade'],
                            'subtotal': item['preco'] * item['quantidade']
                        } for item in itens])
        result_rel.consume()

    for index, item in enumerate(itens):
        query = """
        MATCH (p:Produto {id: $id_produto})
        SET p.quantidade = p.quantidade - $quantidade
        RETURN p
        """
        with session.begin_transaction() as tx:
            tx.run(query, id_produto=item['id'], quantidade=item['quantidade'])
            print(f"Quantidade do produto {item['id']} atualizada com sucesso!")

def listarTodasCompras():
    print("\n======== Listar todas Compras ========")
    query = """
    MATCH (u:Usuario)-[:COMPROU]->(c:Compra), 
          (c)-[r:CONTEM]->(p:Produto)
    RETURN c, u, p, r.quantidade AS quantidade, r.subtotal AS subtotal
    """

    with session.begin_transaction() as tx:
        result = tx.run(query)
        for record in result:
            c = record["c"]
            u = record["u"]
            p = record["p"]
            quantidade = record["quantidade"]
            subtotal = record["subtotal"]

            print("-" * 40)
            print(f"ID Compra: {c['id']}")
            print(f"Data: {c['data']}")
            print(f"Total: {c['valor']}")  
            print(f"Usuário: {u['nome']}")
            print(f"Produto: {p['nome']}")
            print(f"Quantidade: {quantidade}")
            print(f"Subtotal: {subtotal}")
            print("-" * 40)

def mostrarTodasCompras():
    print("\n======== Listar todas Compras ========")
    query = """
    MATCH (u:Usuario)-[:COMPROU]->(c:Compra), 
          (c)-[r:CONTEM]->(p:Produto)
    RETURN c, u, p, r.quantidade AS quantidade, r.subtotal AS subtotal
    """

    with session.begin_transaction() as tx:
        result = tx.run(query)
        compras = []
        for index, record in enumerate(result):
            compras.append(record)
            print(f"{index} - {record['c']['data']}: R${record['c']['valor']} de {record['u']['nome']}")
    return compras

def listarCompra():
    print("\n======== Listar uma Compra ========")

    compras = mostrarTodasCompras()

    opcao = int(input("Index da opção escolhida: "))
    
    try:
        compra_escolhida = compras[opcao]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return
    
    c = compra_escolhida['c']
    u = compra_escolhida['u']
    p = compra_escolhida['p']
    quantidade = compra_escolhida["quantidade"]
    subtotal = compra_escolhida["subtotal"]

    print("-" * 40)
    print(f"ID Compra: {c['id']}")
    print(f"Data: {c['data']}")
    print(f"Total: {c['valor']}")  
    print(f"Usuário: {u['nome']}")
    print(f"Produto: {p['nome']}")
    print(f"Quantidade: {quantidade}")
    print(f"Subtotal: {subtotal}")
    print("-" * 40)
    