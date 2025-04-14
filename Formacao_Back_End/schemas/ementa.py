from pydantic import BaseModel

#Definindo uma ementa para a formação (se houver)
class EmentaSchema(BaseModel):

    formacao_id: int = 1
    texto: str = "Formação sobre metodologias ativas para professores do ensino fundamental"
