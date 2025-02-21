FROM python:3.12.8-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7600

CMD ["streamlit", "run", "app/main.py", "--server.port", "7600"]
