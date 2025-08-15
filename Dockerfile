FROM python:3.12-alpine

RUN apk add --no-cache libc6-compat

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

RUN chmod +x /app/assets/wgcf

CMD ["python", "-u", "main.py"]
