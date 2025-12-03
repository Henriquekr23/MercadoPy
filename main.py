import sqlite3
import bcrypt

conexao = sqlite3.connect("banco.db")
cursor = conexao.cursor()


def login():
    no_usuario = input("Digite seu nome de usuário: ")
    cursor.execute("SELECT * FROM usuario WHERE nome LIKE ?", (no_usuario,))
    resultado = cursor.fetchone()

    if resultado:
        senha = input("Digite sua senha: ").encode()
        senha_hash = resultado[2]

        if bcrypt.checkpw(senha, senha_hash):
            print(f"\nBem vindo, {resultado[1]}")   
            menu(resultado)
        else:
            print("Senha incorreta, tente novamente")
            login()
    else:
        print("Usuário não encontrado.")
        reg = int(input("Deseja criar uma conta?\n (1)Sim (2)Não\nDigite a opção desejada: "))
        if reg == 1:
            registrar()

def registrar():
    nome = input("Digite seu nome: ")
    senha = input("Digite sua senha: ").encode()
    
    # Encriptador de senha
    salt = bcrypt.gensalt()
    senha_hash = bcrypt.hashpw(senha, salt)

    cursor.execute("""
        INSERT INTO usuario (nome, senha_hash, cargo) VALUES (?, ?, 'CLI')
    """, (nome, senha_hash))
    conexao.commit()

    print("Usuário registrado!")
    login()


def menu(usuario):
    id_usuario = usuario[0]
    
    if usuario[3] == 'ADM':
        opcao = int(input("""
    Menu de Administrador:\n
    (1) Cadastrar produto
    (2) Gerenciar usuários
    (3) Sair do sistema\n
    Digite a opção deseja: """))
        if opcao == 1:
            cadastrar_produto(usuario)
        elif opcao == 2:
            gerenciar_usuario(usuario)
    else:
        opcao = int(input("""
    (1) Visualizar produtos
    (2) Adicionar produto ao carrinho
    (3) Visualizar Carrinho
    (4) Sair do sistema\n
    Digite a opção desejada: """))
        if opcao == 1:
            visualizar_produtos(usuario)
        elif opcao == 2:
            adicionar_produto_carrinho(usuario)
        elif opcao == 3:
            visualizar_carrinho(usuario)


def cadastrar_produto(usuario):
    nome = input("Digite o nome do produto: ")
    valor = float(input("Digite o valor do produto: R$"))

    cursor.execute("""
        INSERT INTO produto (no_produto, vl_produto) VALUES (?, ?)
    """, (nome, valor,))
    print("Produto adicionado!")
    conexao.commit()
    menu(usuario)


def gerenciar_usuario(usuario):
    cursor.execute("SELECT id_usuario, nome, cargo FROM usuario")
    usuarios = cursor.fetchall()    

    for user in usuarios:
        id_usuario, nome, cargo = user
        print(f"""
            Código: {id_usuario}
            Nome: {nome}
            Cargo: {cargo}""")

    opcao = int(input("""
    (1) Excluir usuário
    (2) Editar cargo
    (3) Adicionar usuário
    Digite a opção desejada: """))

    if opcao == 1:
        user_excluir = int(input("Digite o código do usuário que deseja excluir: "))
        cursor.execute("""
            DELETE FROM usuario WHERE id_usuario = ?
        """, (user_excluir,))
    elif opcao == 2:
        user_editar = int(input("Digite o código do usuário que deseja editar o cargo: "))
        novo_cargo = input("Digite o novo cargo: ")
        cursor.execute("""
            UPDATE usuario SET cargo = ? WHERE id_usuario = ?
        """, (novo_cargo, user_editar))
        print("Usuário excluído com sucesso")
    elif opcao == 3:
        nome = input("Digite o nome: ")
        senha = input("Digite uma senha: ")
        cargo = input("Digite o cargo: ")

        cursor.execute("""
            INSERT INTO usuario (nome, senha_hash, cargo) VALUES (?, ?, ?)
        """, (nome, senha, cargo))
        print("Usuário criado!")
    
    conexao.commit()
    menu(usuario)


def visualizar_produtos(usuario):
    cursor.execute("""
        SELECT * FROM produto
    """)

    produtos = cursor.fetchall()
    for produto in produtos:
        id_produto, no_produto, vl_produto = produto
        print(f"""
        Código: {id_produto}
        Nome: {no_produto}
        Valor: {vl_produto}
        """)
    menu(usuario)


def adicionar_produto_carrinho(usuario):
    produto = int(input("Digite o código do produto que deseja adicionar ao carrinho: "))
    cursor.execute("""
        INSERT INTO carrinho (id_usuario, id_produto) VALUES (?, ?) 
    """, (usuario[0], produto,))
    conexao.commit()
    opcao = int(input("Item adicionado ao carrinho! Deseja adicionar outro?\n(1)Sim (2)Não\n"))
    if opcao == 1:
        adicionar_produto_carrinho(usuario)
    else:
        menu(usuario)


def visualizar_carrinho(usuario):
    cursor.execute("""
        SELECT
            p.no_produto,
            p.vl_produto,
            COUNT(p.id_produto) AS quantidade
        FROM produto p
        INNER JOIN carrinho ca ON p.id_produto = ca.id_produto
        INNER JOIN usuario cl ON cl.id_usuario = ca.id_usuario
        WHERE cl.id_usuario = ?
        GROUP BY p.id_produto, p.no_produto, p.vl_produto
    """, (usuario[0],))

    valor_total = 0
    carrinho = cursor.fetchall()
    if carrinho:
        for produto in carrinho:
            no_produto, vl_produto, quantidade = produto
            print(f"""
            Produto: {no_produto}
            Valor: {vl_produto}
            Quantidade: {quantidade}
            """)

            valor_total += vl_produto * quantidade

            print(f"Valor total: R${valor_total:.2f}\n")
            opcao = int(input("Deseja fechar o carrinho?\n (1)Sim (2)Não\n"))

            if opcao == 1:
                cursor.execute("""
                    DELETE FROM carrinho WHERE id_usuario = ?
                """, (usuario[0],))
                print("Carrinho fechado!")

    else:
        print("Carrinho vazio.")

    conexao.commit()
    menu(usuario)

login()