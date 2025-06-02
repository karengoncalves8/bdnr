import uuid
from cassandra.cluster import Cluster
from cassandra.cqlengine.usertype import UserType
from cassandra.cqlengine import columns

class Vendedor(UserType):
    id = columns.UUID()
    nome = columns.Text()
    dataNascimento = columns.Text()
    telefone = columns.Text()
    email = columns.Text()
    senha = columns.Text()
    cnpj = columns.Text()
    rua = columns.Text()
    bairro = columns.Text()
    cidade = columns.Text()
    estado = columns.Text()
    cep = columns.Text()

class Produto(UserType):
    id = columns.UUID()
    nome = columns.Text()
    preco = columns.Double()
    quantidade = columns.Integer()
    marca = columns.Text()
    material = columns.Text()
    descricao = columns.Text()
    vendedor = columns.UserDefinedType(Vendedor)

class Usuario(UserType):
    id = columns.UUID()
    nome = columns.Text()
    dataNascimento = columns.Text()
    telefone = columns.Text()
    email = columns.Text()
    senha = columns.Text()
    rua = columns.Text()
    bairro = columns.Text()
    cidade = columns.Text()
    estado = columns.Text()
    cep = columns.Text()

def conectar_cassandra():
    cluster = Cluster(['localhost'])
    session = cluster.connect()

    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS mercadoLivre
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
    """)

    session.shutdown()
    
    session = cluster.connect('mercadolivre')

    session.execute(""" 
        CREATE TABLE IF NOT EXISTS usuario (
            id uuid PRIMARY KEY,
            nome text,
            dataNascimento text,
            telefone text,
            email text,
            senha text,
            rua text,
            bairro text,
            cidade text,
            estado text,
            cep text
        )
    """)

    session.execute(""" 
        CREATE TYPE IF NOT EXISTS Usuario (
            id uuid,
            nome text,
            dataNascimento text,
            telefone text,
            email text,
            senha text,
            rua text,
            bairro text,
            cidade text,
            estado text,
            cep text
        )
    """)

    cluster.register_user_type('mercadolivre', 'usuario', Usuario)

    session.execute("""
        CREATE TABLE IF NOT EXISTS vendedor (
            id uuid PRIMARY KEY,
            nome text,
            dataNascimento text,
            telefone text,
            email text,
            senha text,
            cnpj text,
            rua text,
            bairro text,
            cidade text,
            estado text,
            cep text
        )
    """)

    session.execute(""" 
        CREATE TYPE IF NOT EXISTS vendedor (
            id uuid,
            nome text,
            dataNascimento text,
            telefone text,
            email text,
            senha text,
            cnpj text,
            rua text,
            bairro text,
            cidade text,
            estado text,
            cep text
        )
    """)

    cluster.register_user_type('mercadolivre', 'vendedor', Vendedor)

    session.execute(""" 
        CREATE TYPE IF NOT EXISTS produto (
            id uuid,
            nome text,
            preco double,
            quantidade int,
            marca text,
            material text,
            descricao text,
            vendedor frozen<vendedor>
        )
    """)
    
    session.execute("""
        CREATE TABLE IF NOT EXISTS produto (
            id uuid PRIMARY KEY,
            nome text,
            preco double,
            quantidade int,
            marca text,
            material text,
            descricao text,
            vendedor frozen<vendedor>
        )
    """)

    cluster.register_user_type('mercadolivre', 'produto', Produto)

    session.execute("""
        CREATE TABLE IF NOT EXISTS compra (
            id uuid PRIMARY KEY,
            data text,
            valor double,
            produtos list<frozen<produto>>,
            usuario frozen<usuario>
        )
    """)

    return session