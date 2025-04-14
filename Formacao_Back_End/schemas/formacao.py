from pydantic import BaseModel
from typing import Optional, List
from Formacao_Back_End.model.formacao import Formacao

from .ementa import EmentaSchema

# Definindo a representação da formação quando uma nova formação é inserida no banco


class FormacaoSchema(BaseModel):
    nome: str = "Formação em metodologias ativas."
    tipo: str = "Presencial"
    carga_horaria: int = 5
    preco:  float = 100.50
    atividade: str = "ATIVO"

# Busca definida com base no nome da formação.


class FormacaoBuscaSchema(BaseModel):
    nome: str = "Teste"


# define a como a listagem de formação é retornada
class ListagemFormacaoSchema(BaseModel):
    formacoes: List[FormacaoSchema]


# função retorna uma representação da formação seguindo o schema em FormacaoViewSchema
def apresenta_formacoes(formacoes: List[Formacao]):
    result = []
    for formacao in formacoes:
        result.append({
            "nome": formacao.nome,
            "tipo": formacao.tipo,
            "carga_horaria": formacao.carga_horaria,
            "preco": formacao.preco,
            "atividade": formacao.atividade,
            "ementa": [{"texto": e.texto} for e in formacao.ementas]
        })

    return {"formacoes": result}

# Define o retorno da formação juntamente com sua ementa


class FormacaoViewSchema(BaseModel):
    id: int = 1
    nome: str = "Formação em metodologias ativas."
    tipo: str = "Presencial"
    carga_horaria: int = 5
    preco: float = 100.50
    atividade: str = "ATIVO"
    ementas: List[EmentaSchema]

# Definição do retorno da estrutura de dado após um remoção.


class FormacaoDeleteSchema(BaseModel):
    message: str
    nome: str

# retornando a representação de um produto seguindo o schema definido em FormacaoViewSchema


def apresenta_formacao(formacao: Formacao):
    return {
        "id": formacao.id,
        "nome": formacao.nome,
        "tipo": formacao.tipo,
        "carga_horaria": formacao.carga_horaria,
        "preco": formacao.preco,
        "atividade": formacao.atividade,
        "ementa": [{"texto": e.texto} for e in formacao.ementas]
    }