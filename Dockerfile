FROM python

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "run.py"]
