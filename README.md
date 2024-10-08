### README - Sistema de Análise de Vendas

---

#### Descrição

Esta aplicação em Python utiliza **Flask** para criar uma API que analisa vendas de vendedores a partir de uma planilha Excel. A aplicação lê os dados da planilha, insere essas informações em um banco de dados MySQL, e então permite que você faça consultas sobre os melhores e piores vendedores de cada mês (Abril, Maio ou Junho) através de uma API REST.

---

#### Tecnologias Utilizadas

- **Python**
- **Pandas**
- **SQLAlchemy**
- **MySQL**
- **Flask**
- **pymysql**

---

### Pré-requisitos

Antes de rodar o projeto, você precisará:

1. **MySQL** (ou um cliente de banco de dados como **Laragon**, **XAMPP**, etc.).
2. **Instalar Bibliotecas Python** :
   pip install
3. **Um servidor de banco de dados ativo**. Você pode usar o **Laragon**, **XAMPP** ou seu próprio ambiente MySQL.

---

### Como Configurar e Executar o Projeto

#### 1. Configurar o Banco de Dados

- Certifique-se de que seu cliente de banco de dados MySQL está ativo (pode ser **Laragon**, **XAMPP** ou outra ferramenta).
- Edite as credenciais de acesso ao MySQL no código `index.py`:

  usuario = 'root'  
  senha = ''  
  host = 'localhost'
  banco_de_dados = 'sales'

- Rode a aplicação. O banco de dados será automaticamente criado no MySQL com base nos dados da planilha.

#### 2. Configurar a Planilha de Vendas

- Certifique-se de que você tem uma planilha Excel chamada `vendas.xlsx` no diretório raiz do projeto com a seguinte estrutura:

| Vendedor | Abril | Maio | Junho |
| -------- | ----- | ---- | ----- |
| Carlos   | 57    | 123  | 46    |
| ...      | ...   | ...  | ...   |

- O código lê essa planilha e insere os dados no banco de dados.

#### 3. Rodar a Aplicação

Execute o arquivo `index.py` para iniciar o servidor Flask:

python index.py

A aplicação Flask será iniciada no endereço padrão `http://127.0.0.1:5000`.

#### 5. Testar a API

Você pode testar a API utilizando o **Thunder Client**, **Postman**, ou diretamente no navegador. Por exemplo, para consultar as vendas do mês de Abril, faça a seguinte requisição:

http://127.0.0.1:5000/api/vendas?mes=abril

Isso retornará uma lista de vendedores e suas vendas para o mês selecionado.

Exemplo de resposta:

[
{ "vendedor": "Carlos", "vendas": 57 },
{ "vendedor": "Ana", "vendas": 46 }
]

---

### Observações Importantes

- **Certifique-se de que seu servidor MySQL está ativo**. Se você estiver usando uma ferramenta como **Laragon** ou **XAMPP**, lembre-se de **iniciar o servidor de banco de dados** antes de rodar o projeto.

---

### Como Utilizar a API

Você pode fazer uma requisição GET para a seguinte URL para consultar os dados:

http://127.0.0.1:5000/api/vendas?mes=<nome_do_mes>

Os parâmetros aceitos para `<nome_do_mes>` são: `abril`, `maio` ou `junho`.

---

### Contato

Para mais informações ou dúvidas, entre em contato pelo e-mail: **andersonsilvasouza714@gmail.com**.
