from cassandra.cluster import Cluster

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

    return session