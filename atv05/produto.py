import uuid
from db import conectar_neo4j

session = conectar_neo4j()

def criarProduto():
    print("\n======== Inserindo um novo produto ========")

    nome = input("Nome: ")
    preco = float(input("Preço: "))
    quantidade = int(input("Quantidade: "))
    marca = input("Marca: ")
    material = input("Material: ")
    descricao = input("Descrição: ")

    print("Associe a um vendedor: ")
    query = "MATCH (v:Vendedor) RETURN v "
    with session.begin_transaction() as tx:
        vendedores = list(tx.run(query))
        for index, row in enumerate(vendedores):
            vendedor = row["v"]
            print(f"{index} - {vendedor['nome']} (ID: {vendedor['id']})")


    opcao_vendedor = int(input("Index da opção escolhida: "))
    try:
        vendedor_escolhido = vendedores[opcao_vendedor]
    except IndexError:
        print("Índice inválido!")
        return

    produto_id = str(uuid.uuid4())

    query = """
    CREATE (p:Produto {
        id: $id,
        nome: $nome,
        preco: $preco,
        quantidade: $quantidade,
        marca: $marca,
        material: $material,
        descricao: $descricao
    })
    RETURN p.id
    """
    
    with session.begin_transaction() as tx:
        result = tx.run(query, 
                        id=produto_id,
                        nome=nome,
                        preco=preco,
                        quantidade=quantidade,
                        marca=marca,
                        material=material,
                        descricao=descricao)
        created_id = result.single()[0]

    print(f"Produto criado com sucesso! ID: {created_id}")

    query = """
        MATCH (v:Vendedor {id: $id1}), (p:Produto {id: $id2})
        MERGE (v)-[:VENDE]->(p)
    """

    with session.begin_transaction() as tx:
        result_rel = tx.run(query, id1=vendedor_escolhido["v"]["id"], id2=produto_id)
        result_rel.consume()

    print("Relação de produto e vendedor criada com sucesso!")

def listarTodosProdutos():
    print("\n======== Listar todos produtos ========")
    query = "MATCH (p:Produto) RETURN p"

    with session.begin_transaction() as tx:
        result = tx.run(query)
        for record in result:
            p = record["p"]
            print("-" * 40)
            print("ID:", p.get("id"))
            print("Nome:", p.get("nome"))
            print("Preço:", p.get("preco"))
            print("Quantidade:", p.get("quantidade"))
            print("Marca:", p.get("marca"))
            print("Material:", p.get("material"))
            print("Descrição:", p.get("descricao"))
            print("-" * 40)

def mostrarTodosProdutos():
    query = "MATCH (p)<-[:VENDE]->(v:Vendedor) return v, p"
    with session.begin_transaction() as tx:
        result = tx.run(query)
        produtos = []
        for index, record in enumerate(result):
            produto = record['p']
            vendedor = record['v']

            produtos.append({
                "id": produto["id"],
                "nome": produto["nome"],
                "marca": produto["marca"],
                "preco": produto["preco"],
                "descricao": produto["descricao"],
                "quantidade": produto["quantidade"],
                "material": produto["material"],
                "vendedor_nome": vendedor["nome"],
                "vendedor_cnpj": vendedor["cnpj"]
            })

            print(f"{index} - {record['p']['nome']}")

    return produtos

def listarProduto():
    print("\n======== Listar um Produto ========")
    produtos = mostrarTodosProdutos()

    opcao = int(input("Index da opção escolhida: "))
    
    try:
        produto_escolhido = produtos[opcao]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return
    
    print("ID:", produto_escolhido.get("id"))
    print("Nome:", produto_escolhido.get("nome"))
    print("Preço:", produto_escolhido.get("preco"))
    print("Quantidade:", produto_escolhido.get("quantidade"))
    print("Marca:", produto_escolhido.get("marca"))
    print("Material:", produto_escolhido.get("material"))
    print("Descrição:", produto_escolhido.get("descricao"))
    print("-- Vendedor:")
    print(f"  Nome: {produto_escolhido['vendedor_nome']}")
    print(f"  CNPJ: {produto_escolhido['vendedor_cnpj']}")
