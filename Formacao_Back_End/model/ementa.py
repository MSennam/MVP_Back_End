from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union
from sqlalchemy.orm import relationship

from .base import Base


class Ementa(Base):
    __tablename__ = 'ementa'

    id = Column(Integer, primary_key=True)
    texto = Column(String(2000))
    data_insercao = Column(DateTime, default=datetime.now())

    #Definição do relacionamento entre a ementa da formação e sua respectiva formação.  

    formacao = Column(Integer, ForeignKey("formacao.pk_formacao"), nullable=False)
    formacao_relacionada = relationship("Formacao", back_populates="ementas")

    def __init__(self, texto:str, data_insercao:Union[DateTime, None] = None):
        
        self.texto = texto
        if data_insercao:
            self.data_insercao = data_insercao