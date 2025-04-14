from flask_openapi3 import OpenAPI, Info,  Tag
from flask import redirect, send_from_directory
from urllib.parse import unquote
import os

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from Formacao_Back_End.model import Session, Formacao, Ementa
from logger import logger
from Formacao_Back_End.schemas import *
from flask_cors import CORS

info = Info(title="API Controle de Formação", version="0.0.1")
app = OpenAPI(__name__, info=info)
CORS(app)

#definição de tags para documentação

home_tag = Tag(name="Documentação", description="Seleção de documentação Swagger, Redox ou Rapidoc")
formacao_tag = Tag(name="Formação", description="Adicionar, remover e visualização de formações na base de dados")
ementa_tag = Tag(name="Ementa", description="Adiciona uma ementa a um curso cadastrado na base de dados.")

# redirecionando a tela que permite escolha do tipo de documentação para  /openAPI.
#@app.get('/', tags=[home_tag])
#def home():
    
#    return redirect('/openapi')

# Servindo arquivos do front-end para integração e testes
@app.get("/")
def frontend():
    caminho = os.path.join(os.path.dirname(__file__), "Formacao_Front_End")
    return send_from_directory(caminho, "index.html")

@app.get("/scripts.js")
def js():
    caminho = os.path.join(os.path.dirname(__file__), "Formacao_Front_End")
    return send_from_directory(caminho, "scripts.js")

@app.get("/styles.css")
def css():
    caminho = os.path.join(os.path.dirname(__file__), "Formacao_Front_End")
    return send_from_directory(caminho, "styles.css")

#metodo post para adicionar uma nova formação ao banco
@app.post('/formacao', tags=[formacao_tag],
          responses={"200": FormacaoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_formacao(form: FormacaoSchema):
    
    """retorna apresentação de formações e ementas associadas"""

    formacao = Formacao(
        nome=form.nome,
        tipo=form.tipo,
        carga_horaria=form.carga_horaria,
        preco=form.preco,
        atividade=form.atividade)
    logger.debug(f"Adicionando formação de nome: '{formacao.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(formacao)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado formação de nome: '{formacao.nome}'")
        return apresenta_formacao(formacao), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Já há na base de dados uma formação com o mesmo nome. Por favor, escolha outro nome."
        logger.warning(f"Erro ao adicionar formação '{formacao.nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        session.rollback() # Desfaz a tentativa de inserção no banco, em caso de erro. 
        error_msg = f"Não foi possível salvar a formação. Erro inesperado: {str(e)}"
        logger.warning(f"Erro ao adicionar formação '{formacao.nome}', {error_msg}")
        return {"message": error_msg}, 400


@app.get('/formacoes', tags=[formacao_tag],
         responses={"200": ListagemFormacaoSchema, "404": ErrorSchema})
def get_formacoes():
    """Faz a busca por todos as formacoes cadastradas

    Retorna uma representação da listagem das formacoes.
    """
    logger.debug(f"Buscando formações ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    formacoes = session.query(Formacao).all()

    if not formacoes:
        # se não há formações cadastradas
        return {"formações": []}, 200
    else:
        logger.debug(f"%d formações econtradas" % len(formacoes))
        # retornando  formações
        print(formacoes)
        return apresenta_formacoes(formacoes), 200


@app.get('/formacao', tags=[formacao_tag],
         responses={"200": FormacaoViewSchema, "404": ErrorSchema})
def get_formacao(query: FormacaoBuscaSchema):
    """Faz a busca por uma formação a partir do id da mesma.

    Retorna uma representação das formações e suas respectivas ementas associadas.
    """
    formacao_nome = query.nome
    logger.debug(f"Coletando informações da formação #{formacao_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    formacao = session.query(Formacao).options(joinedload(Formacao.ementas)).filter(Formacao.nome.ilike(f"%{formacao_nome}%")).first()

    if not formacao:
        # se a formação não constar no banco
        error_msg = "Formação não encontrada no banco de dados."
        logger.warning(f"Erro ao buscar formação '{formacao_nome}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Formação econtrada: '{formacao.nome}'")
        # retorna a representação da formação
        return apresenta_formacao(formacao), 200


@app.delete('/formacao', tags=[formacao_tag],
            responses={"200": FormacaoDeleteSchema, "404": ErrorSchema})
def del_formacao(query: FormacaoBuscaSchema):
    """Deleta uma formação a partir do nome informado

    Confirmação de remoção da formação da base de dados.
    """
    formacao_nome = unquote(unquote(query.nome))
    print(formacao_nome)
    logger.debug(f"Deletando dados sobre a formação #{formacao_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção da formação no banco
    count = session.query(Formacao).filter(Formacao.nome == formacao_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado a formação #{formacao_nome}")
        return {"message": "Formação removida com sucesso.", "id": formacao_nome}
    else:
        # se a formação não foi encontrada
        error_msg = "Formação não encontrada na base de dados."
        logger.warning(f"Erro ao deletar a formação #'{formacao_nome}', {error_msg}")
        return {"message": error_msg}, 404


@app.post('/ementa', tags=[ementa_tag],
          responses={"200": FormacaoViewSchema, "404": ErrorSchema})
def add_ementa(form: EmentaSchema):
    """Adiciona uma ementa à uma formação cadastrada na base identificada pelo id

    Mostra uma representação da formações e suas respectivas ementas associadas.
    """
    formacao_id  = form.formacao_id
    logger.debug(f"Adicionando uma ementa à formação #{formacao_id}")
    # criando conexão com a base
    session = Session()
    # buscando a formação
    formacao = session.query(Formacao).filter(Formacao.id == formacao_id).first()

    if not formacao:
        # se a formação não for encontrada
        error_msg = "Formação não encontrada na base de dados."
        logger.warning(f"Erro ao adicionar uma ementa à formação '{formacao_id}', {error_msg}")
        return {"message": error_msg}, 404

    # criando a ementa da formação
    texto = form.texto
    ementa = Ementa(texto=texto)
    ementa.formacao = formacao.id

    # ligando a ementa à formação
    session.add(ementa)
    session.commit()

    formacao = session.query(Formacao).options(joinedload(Formacao.ementas)).filter(Formacao.id == formacao_id).first()
    logger.debug(f"Ementa adicionada à formação #{formacao_id}")

    # apresentando a formação
    return apresenta_formacao(formacao), 200

