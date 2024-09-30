# Use uma imagem base do Python
FROM python:3.9

# Instale o Nginx e o Certbot
RUN apt-get update && apt-get install -y nginx certbot

# Copie os arquivos de configuração do Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Instale as dependências do Python
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copie o código da aplicação
COPY . /app

# Defina o diretório de trabalho
WORKDIR /app

# Comando para rodar o Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]

# Comando para rodar o Nginx
CMD ["nginx", "-g", "daemon off;"]
