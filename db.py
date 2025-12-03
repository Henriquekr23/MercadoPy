import sqlite3

conexao = sqlite3.connect("banco.db")
cursor = conexao.cursor()

# Criação das tabelas do banco
# cursor.execute("""
#     CREATE TABLE usuario(
#         id_usuario INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#         nome TEXT NOT NULL,
#         senha_hash BLOB NOT NULL,
#         cargo TEXT NOT NULL
#     )
# """)

# cursor.execute(""" 
#     CREATE TABLE produto(
#         id_produto INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#         no_produto TEXT NOT NULL,
#         vl_produto FLOAT NOT NULL
#     )
# """)

# cursor.execute("""
#     CREATE TABLE carrinho(
#         id_usuario INTEGER NOT NULL REFERENCES usuario(id_usuario),
#         id_produto INTEGER NOT NULL REFERENCES produto(id_produto)
#     )
# """)

# cursor.execute("""
    # INSERT INTO produto
    # (no_produto, vl_produto) VALUES ('Arroz', 19.90)
# """)
# 
# cursor.execute("""
    # INSERT INTO produto
    # (no_produto, vl_produto) VALUES ('Feijão', 28.50)
# """)

# cursor.execute("""
#     INSERT INTO carrinho
#     (id_usuario, id_produto) VALUES (1, 1)
# """)

cursor.execute("""
    UPDATE usuario
    SET cargo = 'ADM'
    WHERE id_usuario = 1
""")

conexao.commit()