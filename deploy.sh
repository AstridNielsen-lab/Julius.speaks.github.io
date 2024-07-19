#!/bin/bash

echo "Iniciando o deploy da aplicação Flask no servidor de produção..."

# Navegar para o diretório do projeto
cd /path/to/your/project

# Ativar o ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Parar o serviço Gunicorn existente
sudo systemctl stop gunicorn

# Iniciar o Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Iniciar o serviço Gunicorn
sudo systemctl start gunicorn

echo "Deploy concluído."
