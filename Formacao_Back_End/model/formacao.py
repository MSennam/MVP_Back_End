from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from .base import Base
from .ementa import Ementa

class Formacao(Base):
    __tablename__ = 'formacao'

    id = Column("pk_formacao", Integer, primary_key=True)
    nome = Column(String(200), unique=True)
    tipo = Column(String(20))
    carga_horaria = Column(Integer)
    preco = Column(Float)
    atividade = Column(String(15))
    data_insercao = Column(DateTime, default=datetime.now())
    ementas = relationship("Ementa", back_populates="formacao_relacionada")

# torna os modelos acessíveis diretamente do pacote model
__all__ = ["Session", "Formacao", "Ementa"]