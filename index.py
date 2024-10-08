import pandas as pd
from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, text
import pymysql
from flask import Flask, jsonify, request

# Configurações do banco de dados
usuario = 'root'
senha = ''
host = 'localhost'
banco_de_dados = 'sales'

# Conexão com o banco e criação do banco de dados se não existir
conexao = pymysql.connect(host=host, user=usuario, password=senha)
cursor = conexao.cursor()
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {banco_de_dados}")
cursor.close()
conexao.close()

# Conexão com o banco de dados sales
engine = create_engine(f'mysql+pymysql://{usuario}:{senha}@{host}/{banco_de_dados}')
metadata = MetaData()

# Leitura da planilha de vendas
file_path = './vendas.xlsx'
df = pd.read_excel(file_path)

# Verifica os nomes das colunas do DataFrame
print("Colunas lidas da planilha:", df.columns)

# Renomeia as colunas do DataFrame, se necessário, para garantir consistência
df.columns = ['vendedor', 'abril', 'maio', 'junho']

# Criação da tabela de vendas no banco de dados
tabela_vendas = Table('vendas', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('vendedor', String(255)),
    Column('abril', Integer),
    Column('maio', Integer),
    Column('junho', Integer)
)

metadata.create_all(engine)

# Inserção dos dados da planilha no banco de dados
df.to_sql('vendas', engine, if_exists='replace', index=False)

# Criação de uma API fictícia para exibir os dados
app = Flask(__name__)

@app.route('/api/vendas', methods=['GET'])
def get_vendas():
    mes = request.args.get('mes')
    if mes not in ['abril', 'maio', 'junho']:
        return jsonify({'erro': 'Mês inválido! Use abril, maio ou junho.'}), 400
    
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM vendas ORDER BY {mes} DESC"))
        vendas = [{'vendedor': row[1], 'vendas': row[2]} for row in result]  # Acessa pelos índices

    return jsonify(vendas)

# Exibe o melhor e pior vendedor no terminal ao rodar o script
def mostrar_melhor_pior_vendedor(mes):
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT vendedor, {mes} FROM vendas ORDER BY {mes} DESC"))
        vendas = list(result)

        # Acessa o 'vendedor' e o valor de vendas pelo índice da tupla
        melhor_vendedor = vendas[0][0]  # O vendedor está na primeira posição
        pior_vendedor = vendas[-1][0]   # O vendedor do último está na primeira posição

        print(f"O melhor vendedor de {mes.capitalize()} foi {melhor_vendedor}.")
        print(f"O pior vendedor de {mes.capitalize()} foi {pior_vendedor}.")

if __name__ == '__main__':
    mes_analisado = input("Qual mês deseja analisar? (abril, maio ou junho): ").lower()
    if mes_analisado in ['abril', 'maio', 'junho']:
        mostrar_melhor_pior_vendedor(mes_analisado)
    else:
        print("Mês inválido! Use abril, maio ou junho.")
    
    # Inicia a API
    app.run(debug=True)
