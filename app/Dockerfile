FROM python:3.9
ADD . /app
WORKDIR /app
ENV APP_ENV=compose
RUN pip install -r requirements.txt
CMD ["python", "main.py"]