import sqlite3

# Função para criar o Banco de Dados
def createDB():
    db = sqlite3.connect('Ativos.db')
    cs = db.cursor()
    cs.execute(""" CREATE TABLE ativos (
            simbolo TEXT NOT NULL PRIMARY KEY,
            nome TEXT NOT NULL,
            habilitado NUMBER NOT NULL
    )""")

    cs.execute(""" CREATE TABLE precos (
            data TEXT NOT NULL,
            preco REAL NOT NULL,
            simbolo TEXT NOT NULL,
            FOREIGN KEY (simbolo)
                REFERENCES ativos (simbolo)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
    )""")

# Criando o Banco de Dados 
createTable()
