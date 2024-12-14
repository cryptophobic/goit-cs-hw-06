FROM python:3.13-slim

WORKDIR /

COPY . /

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000
EXPOSE 5001

CMD ["python", "main.py"]