import requests
import sqlite3
import datetime as DT


# Função para mudar a coluna 'habilitado' de um ativo
# Logo se o ativo estiver com habilitado = 0, habilitado
# passará a ser 1 e vice-versa

def habilitarAtivo(simbolo):
    # Conectando ao Banco de Dados
    db = sqlite3.connect("Ativos.db")
    cursor = db.cursor()
    
    # Pegando o valor atual de 'habilitado'
    cursor.execute(f"""
    SELECT habilitado FROM ativos WHERE simbolo LIKE '{simbolo}'
    """)
    x = cursor.fetchall()[0][0]

    # Invertendo o valor
    habilitado = int(not x)

    # Atualizando o valor na tabela

    cursor.execute(f""" UPDATE ativos
    SET habilitado = {habilitado}
    WHERE simbolo LIKE '{simbolo}'
    """)

    # Fechando o Banco de Dados
    db.commit()
    db.close()



# Função para o cadastro de ativos no banco de dados
def cadastrarAtivo(simbolo,nome,habilitado):
    
    # Conectando ao Banco de Dados
    db = sqlite3.connect("Ativos.db")
    cursor = db.cursor()
    
    try:
        # Inserindo os valores dos parametros na tabela
        cursor.execute("INSERT INTO ATIVOS (simbolo, nome, habilitado) VALUES (?, ?, ?)",(simbolo,nome,habilitado))

    # Caso o simbolo já esteja cadastrado a função apenas ignora o comando    
    except:
        pass
    
    # Fechando o Banco de Dados
    db.commit()
    db.close()


# Função Responsavel por importar o preço de fechamento dos ativos
#   no dia em que a função foi chamada, além disso
#   a função pegará o preço do ativo nos ultimos 7 dias uteis
# Caso já estajam cadastrados serão atualizados,
#   caso contrario serão inseridos.

def precoAtivo(simbolo):
    # Conectando ao Banco de Dados
    db = sqlite3.connect("Ativos.db")
    cursor = db.cursor()


    # Verificando se a ação está habilitada para importação de preço
    cursor.execute(f"""
    SELECT habilitado FROM ativos WHERE simbolo LIKE '{simbolo}'
    """)
    if cursor.fetchall()[0][0] == 0:
        return

    # Tenta pegar os valores do simbolo passado no parametro
    request = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={simbolo}&apikey=6ENNELNN1EJXX1ZF')
    dados = request.json()

    # Caso não encontre adiciona o sufixo '.SAO' e tenta novamente
    if 'Error Message' in dados.keys():
        simbolo = simbolo + '.SAO'
        request = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={simbolo}&apikey=6ENNELNN1EJXX1ZF')
        dados = request.json()

    # Lista para armazenar os 7 dias uteis anteriores a data atual    
    diasUteis = []
    hoje = DT.datetime.now()

    # Variavel para manipular o loop a seguir
    temp = 0

    # Usando a biblioteca datetime e um loop while
    #   procuramos os 7 dias uteis anteriores a data atual 

    # O que o loop faz é pegar o dia de hoje e diminuir o valor da variavel 'temp'
    #   retornando uma data, essa data será verificada e se for um dia util será
    #   adicionada a lista 'diasUteis' caso contrário será descartada, o valor de 'temp'
    #   aumenta para ver o dia anterior e o loop continua até a lista ter 7 dias úteis 
    while len(diasUteis) != 7:
        day = (hoje-DT.timedelta(days=temp)).strftime("%Y-%m-%d")
        if DT.datetime.strptime(day, '%Y-%m-%d').date().weekday() != 5 and DT.datetime.strptime(day, '%Y-%m-%d').date().weekday() != 6:
            diasUteis.append(day)
        temp+=1

    # Loop para adicionar ou atualizar os valores do ativo na tabela precos
    for date in diasUteis:

        # Aqui pegamos todas as datas cadastradas para aquele ativo
        # e colocamos em uma lista
        cursor.execute(f"""
            SELECT data FROM precos WHERE simbolo LIKE '{simbolo}'
            """)
        ultimasDatas = [i[0] for i in cursor.fetchall()]

        # Se a data não estiver cadastrada para aquele ativo
        # inserimos na tabela
        if date not in ultimasDatas:
            preco = dados['Time Series (Daily)'][date]['4. close']
            cursor.execute("INSERT INTO PRECOS (simbolo, data, preco) VALUES (?, ?, ?)",(simbolo,date,preco))

        # Caso contrário Atualizamos o valor do dia que já estava cadastrado  
        else:
            preco = dados['Time Series (Daily)'][date]['4. close']
            cursor.execute(f"""
            UPDATE precos
            SET preco = {preco}
            WHERE simbolo LIKE '{simbolo}' AND data LIKE '{date}'
            """)

    # Fechando o Banco de Dados        
    db.commit()    
    db.close()

#Teste
cadastrarAtivo('B3SA3.SAO','Bolsa',True)
cadastrarAtivo('PETR4.SAO','Bolsa',True)
precoAtivo('B3SA3.SAO')
precoAtivo('PETR4.SAO')
habilitarAtivo('B3SA3.SAO')
habilitarAtivo('PETR4.SAO')