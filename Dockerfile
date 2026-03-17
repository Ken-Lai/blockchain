FROM python:3.14.2-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY blockchain.py .

EXPOSE 5000

CMD python app.py