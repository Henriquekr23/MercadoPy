import sqlite3

conexao = sqlite3.connect("banco.db")
cursor = conexao.cursor()

def menu(id_usuario):
    opcao = int(input("""
    (1) Visualizar produtos\n
    (2) Adicionar produto ao carrinho\n
    (3) Visualizar Carrinho\n
    Digite a opção desejada: """))
    
    if opcao == 1:
        visualizar_produtos()
    elif opcao == 2:
        adicionar_produto_carrinho(id_usuario)
    elif opcao == 3:
        visualizar_carrinho(id_usuario)

def visualizar_produtos():
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
    menu(id_usuario)

def adicionar_produto_carrinho(id_usuario):
    produto = int(input("Digite o código do produto que deseja adicionar ao carrinho: "))
    cursor.execute("""
        INSERT INTO carrinho (id_usuario, id_produto) VALUES (?, ?) 
    """, (id_usuario, produto,))
    conexao.commit()
    opcao = int(input("Item adicionado ao carrinho! Deseja adicionar outro?\n(1) SIM (2) NÃO\n"))
    if opcao == 1:
        adicionar_produto_carrinho(id_usuario)
    else:
        menu(id_usuario)

def visualizar_carrinho(id_usuario):
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
    """, (id_usuario,))

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
    else:
        print("Carrinho vazio.")

    print(f"    Valor total: R${valor_total}")

    menu(id_usuario)

no_usuario = input("Digite seu nome de usuário: ")
# Acrescentar senha no login
# E conferir se for administrador poder ver mais coisas
cursor.execute("SELECT id_usuario FROM usuario WHERE nome LIKE ?", (no_usuario,))
resultado = cursor.fetchone()

if resultado:
    id_usuario = resultado[0]
    menu(id_usuario)
else:
    print("Usuário não encontrado.")

conexao.commit()