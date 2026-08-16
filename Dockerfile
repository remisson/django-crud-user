FROM python: 3.10
WORKDIR /userservice
COPY . .
RUN pip install -r requirements.txt
CMD ["python","manage.py","runserver"]
