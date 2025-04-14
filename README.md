# MVP - Gerenciador de Formações (baseado no exemplo da Aula 3 da pós graduação em Engenharia de Software da PUC-RJ)

A API tem como intenção ser um gerenciador de formações de uma instituição de ensino, seja pública ou privada.

As formações são constituidas dos seguintes campos: Nome, Tipo, Carga Horária, Preço e se a formação se encontra ativa ou não. 

Também é possível incluir uma ementa para o curso, mas isso não é obrigatório. 

## Executando o programa

Para executar o programa, é necessário possuir todas as bibliotecas contidas no `requirements.txt`. 
Use o comando: pip install -r requirements.txt para instalar as bibliotecas necessárias. 

> É recomendável utilizar um ambiente virtual para rodar a aplicação. Você pode instalar usando o comando: python -m venv nome_do_ambiente_virtual
> Depois basta executar o comando: ./nome_do_ambiente_virtual/scripts/activate
> Repare que haverá uma indicação ao lado da pasta no terminal indicando que você está em um ambiente virtual (env)

Para executar a API, execute o comando:
```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Caso rode no modo desenvolvimento, é recomendável utilizar parâmetro reload, para reiniciar o servidor automáticamente após uma mudança no código. 
```
(env)$ flask run --host 0.0.0.0 --port 5000 -- reload
```

Só abrir o [http://localhost:5000/#/] no navegador para ver a aplicação sendo executada. 


