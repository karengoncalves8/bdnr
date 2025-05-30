from db import conectar_cassandra
import uuid

session = conectar_cassandra()

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

    user_id = uuid.uuid4()

    session.execute("""
        INSERT INTO vendedor (id, nome, dataNascimento, telefone, email, senha, cnpj, rua, bairro, cidade, estado, cep)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (user_id, nome, dataNas, telefone, email, senha, cnpj, rua, bairro, cidade, estado, cep))

    print(f"Vendedor criado com sucesso! ID: {user_id}")

def listarVendedores():
    rows = session.execute("SELECT * FROM vendedor")

    for row in rows:
        print("ID:", row.id)
        print("Nome:", row.nome)
        print("Data de Nascimento:", row.datanascimento)
        print("Telefone:", row.telefone)
        print("Email:", row.email)
        print("Senha:", row.senha)
        print("CNPJ:", row.cnpj)
        print("Rua:", row.rua)
        print("Bairro:", row.bairro)
        print("Cidade:", row.cidade)
        print("Estado:", row.estado)
        print("CEP:", row.cep)

        print("-" * 40)