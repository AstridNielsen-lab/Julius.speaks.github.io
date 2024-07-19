@echo off
echo Iniciando o deploy da aplicação Flask...

:: Ativar o ambiente virtual
call venv\Scripts\activate

:: Instalar dependências
pip install -r requirements.txt

:: Executar o servidor Flask com Waitress (alternativa ao Gunicorn no Windows)
python -m flask run --host=0.0.0.0 --port=8000

echo Deploy concluído.
