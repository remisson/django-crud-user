FROM python:3.10
WORKDIR /userservice
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "userservice/manage.py", "runserver", "0.0.0.0:8000"]
