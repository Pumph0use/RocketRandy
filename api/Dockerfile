FROM python:3.9-alpine
ADD . /api
WORKDIR /api
RUN pip install -r requirements.txt
CMD ["python", "main.py"]