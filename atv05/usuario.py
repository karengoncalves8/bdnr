from db import conectar_neo4j
import uuid

session = conectar_neo4j()

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
    user_id = str(uuid.uuid4()) 

    query = """
    CREATE (u:Usuario {
        id: $id,
        nome: $nome,
        dataNascimento: $dataNascimento,
        telefone: $telefone,
        email: $email,
        senha: $senha,
        rua: $rua,
        bairro: $bairro,
        cidade: $cidade,
        estado: $estado,
        cep: $cep
    })
    RETURN u.id
    """

    with session.begin_transaction() as tx:
        result = tx.run(query,
                        id=user_id,
                        nome=nome,
                        dataNascimento=dataNas,
                        telefone=telefone,
                        email=email,
                        senha=senha,
                        rua=rua,
                        bairro=bairro,
                        cidade=cidade,
                        estado=estado,
                        cep=cep)
        created_id = result.single()[0]
        print(f"Usuário criado com sucesso com ID: {created_id}")

def listarUsuarios():
    query = "MATCH (u:Usuario) RETURN u"

    with session.begin_transaction() as tx:
        result = tx.run(query)
        print("\nListagem de usuários:")
        for record in result:
            u = record["u"]
            print("-" * 40)
            print("ID:", u.get("id"))
            print("Nome:", u.get("nome"))
            print("Data de Nascimento:", u.get("dataNascimento"))
            print("Telefone:", u.get("telefone"))
            print("Email:", u.get("email"))
            print("Senha:", u.get("senha"))
            print("  Rua:", u.get("rua"))
            print("  Bairro:", u.get("bairro"))
            print("  Cidade:", u.get("cidade"))
            print("  Estado:", u.get("estado"))
            print("  CEP:", u.get("cep"))
            print("-" * 40)

def mostrarTodosUsuarios():
    query = """
    MATCH (u:Usuario)-[:COMPROU]->(c:Compra)
    MATCH (c)-[r:CONTEM]->(p:Produto)
    MATCH (p)<-[:VENDE]->(v:Vendedor)
    RETURN u, c, collect({produto: p, quantidade: r.quantidade, subtotal: r.subtotal, vendedor: v}) AS produtos
    """

    with session.begin_transaction() as tx:
        result = tx.run(query)
        usuarios_com_compras = {}

        for index, record in enumerate(result):
            usuario = record["u"]  # Acessando o nó Usuario
            compra = record["c"]  # Acessando o nó Compra
            produtos = record["produtos"]  # Acessando os produtos e vendedores associados à compra

            # Verifica se o usuário já está no dicionário de usuários com compras
            if usuario["id"] not in usuarios_com_compras:
                usuarios_com_compras[usuario["id"]] = {
                    'usuario': usuario,
                    'compras': []
                }

            # Adiciona os detalhes da compra ao usuário
            compra_completa = {
                "compra_id": compra["id"],
                "data": compra["data"],
                "produtos": []
            }

            # Adiciona os produtos e vendedores à lista de produtos dessa compra
            for produto_info in produtos:
                produto = produto_info["produto"]
                vendedor = produto_info["vendedor"]
                compra_completa["produtos"].append({
                    "produto_nome": produto["nome"],
                    "quantidade": produto_info["quantidade"],
                    "subtotal": produto_info["subtotal"],
                    "vendedor_nome": vendedor["nome"]
                })

            # Adiciona a compra completa ao usuário
            usuarios_com_compras[usuario["id"]]["compras"].append(compra_completa)

        # Convertendo o dicionário para uma lista antes de retornar
        usuarios_com_compras_list = list(usuarios_com_compras.values())

        for index, usuario_info in enumerate(usuarios_com_compras_list):
            print(f'{index} - {usuario_info["usuario"]["nome"]}')

    return usuarios_com_compras_list

def listarUsuario():
    print("\n======== Listar um Usuario ========")
    usuarios = mostrarTodosUsuarios()

    opcao = int(input("Index da opção escolhida: "))
    
    try:
        usuario_escolhido = usuarios[opcao]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return
    
    u = usuario_escolhido.get("usuario")

    print("uxuario", usuario_escolhido)
    
    print("ID:", u.get("id"))
    print("Nome:", u.get("nome"))
    print("Data de Nascimento:", u.get("dataNascimento"))
    print("Telefone:", u.get("telefone"))
    print("Email:", u.get("email"))
    print("Senha:", u.get("senha"))
    print("  Rua:", u.get("rua"))
    print("  Bairro:", u.get("bairro"))
    print("  Cidade:", u.get("cidade"))
    print("  Estado:", u.get("estado"))
    print("  CEP:", u.get("cep"))
    print("-- Compras:")
    for compra in usuario_escolhido.get("compras"):
        print("-" * 40)
        print(f"  Compra ID: {compra['compra_id']}")
        print(f"  Data: {compra['data']}")
        for produto in compra["produtos"]:
            print(f"    Produto: {produto['produto_nome']}")
            print(f"    Quantidade: {produto['quantidade']}")
            print(f"    Subtotal: {produto['subtotal']}")
            print(f"    Vendedor: {produto['vendedor_nome']}")
        print("-" * 40)
