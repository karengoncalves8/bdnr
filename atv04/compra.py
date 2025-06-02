import uuid
from db import Usuario, conectar_cassandra, Produto
from produto import mostrarTodosProdutos
from usuario import mostrarTodosUsuarios

session = conectar_cassandra()

def mostrarTodasCompras():
    print("\nListagem de Compras")
    compras = session.execute("SELECT * FROM compra")
    for index, compra in enumerate(compras):
        print(f'{index} - {compra.usuario.nome} - {compra.data}: R${compra.valor}')

def listarCompraDict(compra):
    for key, value in compra._asdict().items():
        if key == "produtos":
            print("-- Produtos: ")
            for item_compra in value:
                print(f"> {item_compra.nome} | Quantidade: {item_compra.quantidade} | Subtotal: {item_compra.preco * item_compra.quantidade}")
            continue
        if key == "usuario":
            print(f'{key}: {value.nome}')
            continue
        print(f'{key}: {value}')

def criarCompra():
    print("\n======== Inserindo uma nova compra ========")

    data = input("Data: ")

    print("Escolha os produtos e sua quantidade: ")
    itens = []
    produtos_comprados = []

    while True:
        mostrarTodosProdutos()

        opcao_produto = int(input("Index da opção escolhida: "))
        produtos = list(session.execute("SELECT * FROM produto"))

        try:
            produto_escolhido = produtos[opcao_produto]
        except IndexError:
            print("Índice não encontrado! Por favor, escolha um índice válido.")
            return
        
        while True:
            quantidade = int(input(f"Quantidade (disponível: {produto_escolhido.quantidade}): "))

            if quantidade > produto_escolhido.quantidade: 
                print(f"Quantidade indisponível.")
            else:
                break
            
        item_compra = Produto(
            id=produto_escolhido.id,
            nome=produto_escolhido.nome,
            preco=produto_escolhido.preco,
            quantidade=quantidade,
            marca=produto_escolhido.marca,
            material=produto_escolhido.material,
            descricao=produto_escolhido.descricao,
            vendedor=produto_escolhido.vendedor
        )

        itens.append(item_compra)
        produtos_comprados.append(produto_escolhido)
        
        escolha = input("Deseja adicionar mais produtos? [S/N] ")
        if escolha.lower() in ['n', 'nao', 'não']: 
            break

    print('Associe essa compra a um usuário: ')
    mostrarTodosUsuarios()

    usuario_opcao = int(input("Index da opção escolhida: "))
    usuarios = list(session.execute("SELECT * FROM usuario"))

    try:
        usuario_escolhido = usuarios[usuario_opcao]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return
    
    total_sugerido = 0
    for item in itens:
        total_sugerido += item.preco * item.quantidade

    valor = float(input(f"Valor total (calculado: {total_sugerido}): "))
    
    compra_id = uuid.uuid4()
    usuario_obj = Usuario(
        id=usuario_escolhido.id,
        nome=usuario_escolhido.nome,
        dataNascimento=usuario_escolhido.datanascimento,
        telefone=usuario_escolhido.telefone,
        email=usuario_escolhido.email,
        senha=usuario_escolhido.senha,
        rua=usuario_escolhido.rua,
        bairro=usuario_escolhido.bairro,
        cidade=usuario_escolhido.cidade,
        estado=usuario_escolhido.estado,
        cep=usuario_escolhido.cep
    )

    session.execute("""
        INSERT INTO compra (id, data, valor, produtos, usuario)
        VALUES (%s, %s, %s, %s, %s)
    """, (compra_id, data, valor, itens, usuario_obj))

    print(f"Compra criada com sucesso! ID: {compra_id}")

    for index, item in enumerate(itens):
        session.execute("""
            UPDATE produto SET quantidade=%s WHERE id=%s
        """, (produtos_comprados[index].quantidade - item.quantidade, item.id))
        print(f"Quantidade do produto {item.nome} atualizada com sucesso!")

def deletarCompra():
    print("\n======== Remover uma Compra ========")

    mostrarTodasCompras()

    opcao = int(input("Index da opção escolhida: "))

    compras = list(session.execute("SELECT * FROM compra"))
    try:
        compra_escolhida = compras[opcao]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return

    session.execute("""
        DELETE FROM compra WHERE id = %s
    """, (compra_escolhida.id))

    print("Compra deletada com sucesso!")

def listarTodasCompras():
    print("\n======== Listar toda as Compras ========")
    compras = session.execute("SELECT * FROM compra")
    
    for compra in compras:
        print("------------------------------------------------------")
        listarCompraDict(compra)
