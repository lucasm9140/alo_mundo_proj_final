
from flask import Flask, render_template,request
# Lista de Importação#
# Importa a função `sessionmaker`, que é usada para criar uma nova sessão para interagir com o banco de dados
from sqlalchemy.orm import sessionmaker

# Importa as funções `create_engine` para estabelecer uma conexão com o banco de dados e `MetaData` para trabalhar com metadados do banco de dados
from sqlalchemy import create_engine, MetaData

# Importa a função `automap_base`, que é usada para refletir um banco de dados existente em classes ORM automaticamente
from sqlalchemy.ext.automap import automap_base
from aluno import Aluno


app = Flask(__name__)

#Conexão e Mapeamento#

# Criando a configuração do banco de dados
# Configuração do Banco de Dados
# biblioteca para converter e resolver problema do @
import urllib.parse

# Qual o usuário do banco e a senha?
user = 'lucas'
password = urllib.parse.quote_plus('')

host = 'localhost'
database = 'school'
connection_string = f'mysql+pymysql://{user}:{password}@{host}/{database}'

# Criar a engine e refletir o banco de dados existente
engine = create_engine(connection_string)
metadata = MetaData()
metadata.reflect(engine)

# Mapeamento automático das tabelas para classes Python
Base = automap_base(metadata=metadata)
Base.prepare()

# Acessando a tabela 'aluno' mapeada
Aluno = Base.classes.aluno

# Criar a sessão do SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()


@app.route("/inicio")
def index():
    return render_template("index.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route('/novoaluno',methods=['POST'])
def inserir_aluno():
    ra = request.form['ra']
    nome = request.form['nome']
    rendafamiliar = request.form['rendafamiliar']
    tempoestudo = request.form['tempoestudo']

    # sessão ok
    alunos = Aluno(ra=ra,nome=nome,renda_familiar=rendafamiliar,tempo_estudo=tempoestudo)

    try:
        session.add(alunos)
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()
    mensagem = "cadastrado com sucesso"
    
    return render_template('index.html',mensagem=mensagem)

if __name__ == "__main__":
    app.run(debug=True)
