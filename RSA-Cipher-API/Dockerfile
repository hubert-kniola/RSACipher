FROM python:3.10.0a7-buster

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY /RSA-Cipher-API .

CMD ["uvicorn", "RSA-Cipher-API.api:app", "--host", "0.0.0.0", "--port", "8000"]