from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# importando os elementos definidos no modelo
from .base import Base
from .ementa import Ementa
from .formacao import Formacao

# Caminho absoluto até a raiz do projeto
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Caminho absoluto para a pasta do banco de dados
db_path = os.path.join(base_dir, "database")

# Cria a pasta se ela não existir
if not os.path.exists(db_path):
    os.makedirs(db_path)

# Caminho absoluto completo para o SQLite
db_url = f"sqlite:///{os.path.join(db_path, 'db.sqlite3')}"

# cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)

# cria o banco se ele não existir 
if not database_exists(engine.url):
    create_database(engine.url) 

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)

# torna os modelos acessíveis diretamente do pacote model
__all__ = ["Session", "Formacao", "Ementa"]