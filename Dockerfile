FROM python:3.10

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o conteúdo da pasta src para dentro de /app
COPY src/ /app/

EXPOSE 8000

CMD ["sh", "-c", "python /app/manage.py makemigrations && python /app/manage.py migrate && python /app/manage.py collectstatic --noinput && gunicorn --workers 3 --timeout 120 --bind 0.0.0.0:8000 userservice.wsgi:application"]
