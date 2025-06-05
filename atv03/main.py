from usuario import criarUsuario, deletarUsuario, editarUsuario, listarTodosUsuarios, listarUsuario
from vendedor import criarVendedor, deletarVendedor, editarVendedor, listarTodosVendedores, listarVendedor
from produto import criarProduto, editarProduto, deletarProduto, listarProduto, listarTodosProdutos
from compra import criarCompra, editarCompra, deletarCompra, listarCompra, listarTodasCompras
from favoritos import criarFavorito, editarFavorito, deletarFavorito, listarFavorito, listarTodosFavoritos
from sincBDs import sinc_bds
from sessao import verificarSessao, verificarUsuarios, login, logout

usuario_email = None

def menuAcoes():
    global usuario_email
    sessao_ativa = verificarSessao(usuario_email)
    
    if not sessao_ativa:
        print("Sessão encerrada. Faça login novamente")
        usuario_email = None
        inicio()
            
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

def main():
    while True:
        global usuario_email
        sessao_ativa = verificarSessao(usuario_email)
        
        if not sessao_ativa:
            print("Sessão encerrada. Faça login novamente")
            usuario_email = None
            inicio()
            break  
            
        print('\nQual coleção deseja gerenciar?')
        print('''
            1 - Usuário
            2 - Vendedor
            3 - Produto
            4 - Compra
            5 - Favorito
            6 - Sincronizar Redis com o MongoDB 
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
                acao = menuAcoes()
                match acao:
                    case 1:
                        criarProduto()
                    case 2:
                        editarProduto()
                    case 3:
                        deletarProduto()
                    case 4:
                        listarProduto()
                    case 5:
                        listarTodosProdutos()
            case 4:
                acao = menuAcoes()
                match acao:
                    case 1:
                        criarCompra()
                    case 2:
                        editarCompra()
                    case 3:
                        deletarCompra()
                    case 4:
                        listarCompra()
                    case 5:
                        listarTodasCompras()
            case 5:
                acao = menuAcoes()
                match acao:
                    case 1:
                        criarFavorito()
                    case 2:
                        editarFavorito()
                    case 3:
                        deletarFavorito()
                    case 4:
                        listarFavorito()
                    case 5:
                        listarTodosFavoritos()
            case 6:
                print("\n======== Atualizando MongoDB com Redis ========")
                sinc_bds()
            case 0:
                logout(usuario_email)
                break
            case _:
                print('Opção não entendida!')

def inicio():
    print('-------- Mercado Livre -----------')
    verificarUsuarios()
    
    global usuario_email
    
    execucao = True
    
    while execucao:
        print(''' O que deseja fazer?
    1 - Login
    2 - Cadastro
    0 - Encerrar aplicação 
        ''')
        
        escolha = int(input('Opção escolhida: '))

        match escolha:
            case 1:
                print("Faça seu login para entrar no sistema:")
                email = input(("Digite seu email: "))
                senha = input(("Digite sua senha: "))
                
                is_authenticated = login(email, senha)
                
                if is_authenticated:
                    print("Login realizado com sucesso!")
                    usuario_email = email
                    
                    execucao = False
                    
                    main()
            case 2:
                criarUsuario()
            case 0:
                print("Encerrando....")
                execucao = False
            case _:
                print('Opção não entendida!')

inicio()
            