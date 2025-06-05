from usuario import criarUsuario, listarUsuarios, listarUsuario
from vendedor import criarVendedor, listarVendedores, listarVendedor
from produto import criarProduto, listarTodosProdutos, listarProduto
from compra import criarCompra, listarTodasCompras, listarCompra

print('-------- Gerenciamento do MongoDB -----------')

def menuAcoes():
    print('\nO que deseja fazer?')
    print('''
        1 - Criar
        2 - Listar todos 
        3 - Listar específico
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
        0 - Sair
    ''')

    escolha = int(input('Opção escolhida: '))

    if escolha == 1:
        acao = menuAcoes()
        if acao == 1:
            criarUsuario()
        elif acao == 2:
            listarUsuarios()
        elif acao == 3:
            listarUsuario()
    elif escolha == 2:
        acao = menuAcoes()
        if acao == 1:
            criarVendedor()
        elif acao == 2:
            listarVendedores()
        elif acao == 3:
            listarVendedor()
    elif escolha == 3:
        acao = menuAcoes()
        if acao == 1:
            criarProduto()
        elif acao == 2:
            listarTodosProdutos()
        elif acao == 3:
            listarProduto()
    elif escolha == 4:
        acao = menuAcoes()
        if acao == 1:
            criarCompra()
        elif acao == 2:
            listarTodasCompras()
        elif acao == 3:
            listarCompra()
    elif escolha == 0:
        break
    else:
        print('Opção não entendida!')
