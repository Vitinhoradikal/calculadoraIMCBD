import sqlite3

con = sqlite3.connect('dados.db')
cur = con.cursor()

tabela = '''CREATE TABLE dados (
                id INTEGER PRIMARY KEY,
                nome VARCHAR(100),
                endereco VARCHAR(100),
                altura REAL,
                peso REAL,
                imc REAL
            )'''

cur.execute(tabela)

con.close()

print('Banco de dados criado com sucesso')