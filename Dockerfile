FROM locustio/locust
COPY . .
RUN pip install -r requirements.txt
