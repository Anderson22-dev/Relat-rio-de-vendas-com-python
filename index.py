import pandas as pd
from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, text
import pymysql
from flask import Flask, jsonify, request


usuario = 'root'
senha = ''
host = 'localhost'
banco_de_dados = 'sales'


conexao = pymysql.connect(host=host, user=usuario, password=senha)
cursor = conexao.cursor()
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {banco_de_dados}")
cursor.close()
conexao.close()


engine = create_engine(f'mysql+pymysql://{usuario}:{senha}@{host}/{banco_de_dados}')
metadata = MetaData()


file_path = './vendas.xlsx'
df = pd.read_excel(file_path)


print("Colunas lidas da planilha:", df.columns)


df.columns = ['vendedor', 'abril', 'maio', 'junho']


tabela_vendas = Table('vendas', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('vendedor', String(255)),
    Column('abril', Integer),
    Column('maio', Integer),
    Column('junho', Integer)
)

metadata.create_all(engine)


df.to_sql('vendas', engine, if_exists='replace', index=False)


app = Flask(__name__)

@app.route('/api/vendas', methods=['GET'])
def get_vendas():
    mes = request.args.get('mes')
    if mes not in ['abril', 'maio', 'junho']:
        return jsonify({'erro': 'Mês inválido! Use abril, maio ou junho.'}), 400
    
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM vendas ORDER BY {mes} DESC"))
        vendas = [{'vendedor': row[1], 'vendas': row[2]} for row in result]  

    return jsonify(vendas)


def mostrar_melhor_pior_vendedor(mes):
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT vendedor, {mes} FROM vendas ORDER BY {mes} DESC"))
        vendas = list(result)


        melhor_vendedor = vendas[0][0]
        pior_vendedor = vendas[-1][0]

        print(f"O melhor vendedor de {mes.capitalize()} foi {melhor_vendedor}.")
        print(f"O pior vendedor de {mes.capitalize()} foi {pior_vendedor}.")

if __name__ == '__main__':
    mes_analisado = input("Qual mês deseja analisar? (abril, maio ou junho): ").lower()
    if mes_analisado in ['abril', 'maio', 'junho']:
        mostrar_melhor_pior_vendedor(mes_analisado)
    else:
        print("Mês inválido! Use abril, maio ou junho.")
    

    app.run(debug=True)
