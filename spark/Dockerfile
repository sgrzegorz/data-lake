FROM bitnami/spark:3.1.1
#spark-base/spark-py:1.0.0
USER root

WORKDIR /app


COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY main.py .

CMD ["echo","Hello World... from my my Spark Image"]
CMD ["python3","/app/main.py"]
