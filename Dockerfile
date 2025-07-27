FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get upgrade -y && apt-get clean

WORKDIR /app/src

# Copia o requirements.txt que está na raiz (fora do src)
COPY requirements.txt /app/requirements.txt

#ATUALIZA O PIP
RUN pip install --no-cache-dir --upgrade pip

# Instala as libs
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copia todo o conteúdo da pasta src para /app/src
COPY ./src /app/src

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
