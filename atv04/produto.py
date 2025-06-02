import uuid
from db import Vendedor, conectar_cassandra

session = conectar_cassandra()

def mostrarTodosProdutos():
    print("\nListagem de Produtos")
    rows = session.execute("SELECT id, nome FROM produto")
    for index, row in enumerate(rows):
        print(f"{index} - {row.nome}")

def listarProdutoDict(produto):
    for key, value in produto._asdict().items():
        if key == "vendedor":
            print("-- Informações do vendedor:")
            vendedor = value
            for vend_key, vend_val in vendedor.items():
                print(f"{vend_key}: {vend_val}")
            continue
        print(f"{key}: {value}")

def criarProduto():
    print("\n======== Inserindo um novo produto ========")

    nome = input("Nome: ")
    preco = float(input("Preço: "))
    quantidade = int(input("Quantidade: "))
    marca = input("Marca: ")
    material = input("Material: ")
    descricao = input("Descrição: ")

    print("Associe a um vendedor: ")
    vendedores = list(session.execute("SELECT * FROM vendedor"))
    for idx, v in enumerate(vendedores):
        print(f"{idx} - {v.nome}")

    opcao_vendedor = int(input("Index da opção escolhida: "))
    try:
        vendedor_escolhido = vendedores[opcao_vendedor]
    except IndexError:
        print("Índice inválido!")
        return

    produto_id = uuid.uuid4()
    
    vendedor_obj = Vendedor(
        id=vendedor_escolhido.id,
        nome=vendedor_escolhido.nome,
        dataNascimento=vendedor_escolhido.datanascimento,
        telefone=vendedor_escolhido.telefone,
        email=vendedor_escolhido.email,
        senha=vendedor_escolhido.senha,
        cnpj=vendedor_escolhido.cnpj,
        rua=vendedor_escolhido.rua,
        bairro=vendedor_escolhido.bairro,
        cidade=vendedor_escolhido.cidade,
        estado=vendedor_escolhido.estado,
        cep=vendedor_escolhido.cep
    )
    session.execute("""
        INSERT INTO produto (id, nome, preco, quantidade, marca, material, descricao, vendedor)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (produto_id, nome, preco, quantidade, marca, material, descricao, vendedor_obj))

    print(f"Produto criado com sucesso! ID: {produto_id}")

def listarProduto():
    print("\n======== Listar um produto ========")

    mostrarTodosProdutos()
    opcao = int(input("Index da opção escolhida: "))

    produtos = list(session.execute("SELECT * FROM produto"))
    try:
        produto_escolhido = produtos[opcao]
    except IndexError:
        print("Índice inválido!")
        return

    listarProdutoDict(produto_escolhido)

def listarTodosProdutos():
    print("\n======== Listar todos produtos ========")
    produtos = session.execute("SELECT * FROM produto")
    
    for produto in produtos:
        print("------------------------------------------------------")
        listarProdutoDict(produto)
