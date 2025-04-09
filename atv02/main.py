from usuario import criarUsuario, deletarUsuario, editarUsuario, listarTodosUsuarios, listarUsuario
from vendedor import criarVendedor, deletarVendedor, editarVendedor, listarTodosVendedores, listarVendedor


print('-------- Gerenciamento do MongoDB -----------')

def menuAcoes():
    print('\nO que deseja fazer?')
    print('''
        1 - Criar
        2 - Atualizar
        3 - Deletar
        4 - Listar específico
        5 - Listar todos 
        0 - Sair
    ''')
    escolha = int(input('Opção escolhida: '))
    return escolha


while True:
    print('\nQual coleção deseja gerenciar?')
    print('''
        1 - Usuário
        2 - Vendedor
        3 - Produto
        4 - Compra
        5 - Favorito
        0 - Sair
    ''')

    escolha = int(input('Opção escolhida: '))

    match escolha:
        case 1:
            acao = menuAcoes()
            match acao:
                case 1:
                    criarUsuario()
                case 2:
                    editarUsuario()
                case 3:
                    deletarUsuario()
                case 4:
                    listarUsuario()
                case 5:
                    listarTodosUsuarios()
        case 2:
            acao = menuAcoes()
            match acao:
                case 1:
                    criarVendedor()
                case 2:
                    editarVendedor()
                case 3:
                    deletarVendedor()
                case 4:
                    listarVendedor()
                case 5:
                    listarTodosVendedores()
        case 3:
            print('hi')
            
        case 4:
            print('hi')
            
        case 5:
            print('hi')
            
        case 0:
            break
        case _:
            print('Opção não entendida!')



