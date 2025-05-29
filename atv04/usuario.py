from db import conectar_cassandra
import uuid

session = conectar_cassandra()

def mostrarTodosUsuarios():
    print("\nListagem de usuário")
    usuarios =  list(session.execute('SELECT * FROM usuario'))

    for index, usuario in enumerate(usuarios):
        print(f'{index} - {usuario.nome}')

def listarUsuarioDict(usuario_dict):
    for key in usuario_dict:
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
    user_id = uuid.uuid4()

    query = """
        INSERT INTO usuario (id, nome, dataNascimento, telefone, email, senha, rua, bairro, cidade, estado, cep)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    session.execute(query, (user_id, nome, dataNas, telefone, email, senha, rua, bairro, cidade, estado, cep))
    print("Usuário criado com sucesso")

def editarUsuario():
    print("\n======== Editar um usuário ========")

    mostrarTodosUsuarios()

    opcao = int(input("Index da opção escolhida: "))

    usuarios =  list(session.execute('SELECT * FROM usuario'))
    try:
        usuario_escolhido = usuarios[opcao]
    except IndexError:
        print("Índice não encontrado! Por favor, escolha um índice válido.")
        return

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

    session.execute("""
        UPDATE usuario SET nome=%s, dataNascimento=%s, telefone=%s, email=%s, senha=%s, rua=%s, bairro=%s, cidade=%s, estado=%s, cep=%s  WHERE id=%s
    """, (nome, dataNas, telefone, email, senha, rua, bairro, cidade, estado, cep, usuario_escolhido.id))

    print("Usuário atualizado com sucesso!")