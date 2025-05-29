from usuario import criarUsuario, editarUsuario
# from vendedor import criarVendedor
# from produto import criarProduto, listarProduto, listarTodosProdutos
# from compra import criarCompra, deletarCompra

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
        0 - Sair
    ''')

    escolha = int(input('Opção escolhida: '))

    if escolha == 1:
        acao = menuAcoes()
        if acao == 1:
            criarUsuario()
        elif acao == 2:
            editarUsuario()
    # elif escolha == 2:
    #     acao = menuAcoes()
    #     if acao == 1:
    #         criarVendedor()
    # elif escolha == 3:
    #     acao = menuAcoes()
    #     if acao == 1:
    #         criarProduto()
    #     elif acao == 4:
    #         listarProduto()
    #     elif acao == 5:
    #         listarTodosProdutos()
    # elif escolha == 4:
    #     acao = menuAcoes()
    #     if acao == 1:
    #         criarCompra()
    #     elif acao == 3:
    #         deletarCompra()
    elif escolha == 0:
        break
    else:
        print('Opção não entendida!')
