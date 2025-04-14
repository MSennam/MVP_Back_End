from pydantic import BaseModel

#Classe definindo mensagem de erro
class ErrorSchema(BaseModel):
    
    message: str
