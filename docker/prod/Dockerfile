FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/requirements.txt


RUN pip install -r requirements.txt

COPY . /app

# RUN chmod +x /app/scripts/start-prod.sh

EXPOSE 5000

CMD ["/app/scripts/start-prod.sh"]

