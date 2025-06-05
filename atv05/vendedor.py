from db import conectar_neo4j
import uuid

session = conectar_neo4j()

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

    user_id = str(uuid.uuid4())

    query = """
    CREATE (v:Vendedor {
        id: $id,
        nome: $nome,
        dataNascimento: $dataNascimento,
        telefone: $telefone,
        email: $email,
        senha: $senha,
        cnpj: $cnpj,
        rua: $rua,
        bairro: $bairro,
        cidade: $cidade,
        estado: $estado,
        cep: $cep
    })
    RETURN v.id
    """

    with session.begin_transaction() as tx:
        result = tx.run(query, 
                        id=user_id,
                        nome=nome,
                        dataNascimento=dataNas,
                        telefone=telefone,
                        email=email,
                        senha=senha,
                        cnpj=cnpj,
                        rua=rua,
                        bairro=bairro,
                        cidade=cidade,
                        estado=estado,
                        cep=cep)
        created_id = result.single()[0]

    print(f"Vendedor criado com sucesso! ID: {created_id}")
    
def mostrarTodosVendedores():
    query = """
    MATCH (v:Vendedor)-[:VENDE]->(p:Produto)
    RETURN v, collect(p) AS produtos
    """

    with session.begin_transaction() as tx:
        result = tx.run(query)
        vendedores = []
        for index, record in enumerate(result):
            vendedor = record["v"]
            produtos = record["produtos"]
            vendedores.append({'v': vendedor, 'p': produtos})
            print(f"{index} - {vendedor['nome']}")
        return vendedores

def listarVendedor():
    print("\n======== Listar um Vendedor ========")
    vendedores = mostrarTodosVendedores()

    opcao = int(input("Index da opção escolhida: "))
    
    try:
        vendedor_escolhido = vendedores[opcao]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return
    
    v = vendedor_escolhido['v']
    produtos = vendedor_escolhido['p']

    print("-" * 40)
    print("ID:", v.get("id"))
    print("Nome:", v.get("nome"))
    print("Data de Nascimento:", v.get("dataNascimento"))
    print("Telefone:", v.get("telefone"))
    print("Email:", v.get("email"))
    print("Senha:", v.get("senha"))
    print("CNPJ:", v.get("cnpj"))
    print("  Rua:", v.get("rua"))
    print("  Bairro:", v.get("bairro"))
    print("  Cidade:", v.get("cidade"))
    print("  Estado:", v.get("estado"))
    print("  CEP:", v.get("cep"))
    print("-- Produtos: ")
    if produtos:
        for produto in produtos:
            print(f'---> {produto.get("nome")}, {produto.get("marca")} - R${produto.get("preco")}')
    else:
        print("Nenhum produto encontrado para esse vendedor.")
    print("-" * 40)

def listarVendedores():
    print("\n======== Listar todos vendedores ========")
    query = "MATCH (v:Vendedor) RETURN v"

    with session.begin_transaction() as tx:
        result = tx.run(query)
        for record in result:
            v = record["v"]
            print("-" * 40)
            print("ID:", v.get("id"))
            print("Nome:", v.get("nome"))
            print("Data de Nascimento:", v.get("dataNascimento"))
            print("Telefone:", v.get("telefone"))
            print("Email:", v.get("email"))
            print("Senha:", v.get("senha"))
            print("CNPJ:", v.get("cnpj"))
            print("  Rua:", v.get("rua"))
            print("  Bairro:", v.get("bairro"))
            print("  Cidade:", v.get("cidade"))
            print("  Estado:", v.get("estado"))
            print("  CEP:", v.get("cep"))
            print("-" * 40)