# Eurofarma app
Projeto do challenge da FIAP 2024
# Como usar
Tenha python e docker instalado em seu computador. Inicie clonando o repo e abrindo no VsCode.
## Criando ambiente virtual
Crie um ambiente virtual e entre nele.
```console
python -m venv .venv
source .venv/Scripts/activate
```
## Instalando dependências
Dentro do ambiente virtual instale as bibliotecas necessárias.
```console
pip install -r requirements.txt
```
## Criando container com MongoDB
Para o banco de dados usaremos um container com MongoDB
```console
docker compose up -d
```
## Rodando a aplicação
Para rodar nossa aplicação apenas utilize:
```console
python app.py
```
E acesse seu navegador na página do [localhost](http://localhost:5000)
