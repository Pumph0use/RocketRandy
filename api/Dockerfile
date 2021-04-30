FROM python:3.9
ADD . /api
WORKDIR /api
ENV FLASK_APP=app
ENV FLASK_ENV=development
ENV APP_ENV=compose
ENV PYTHONUNBUFFERED=1
RUN pip install -e .
RUN pip install -r requirements.txt
CMD ["flask", "run", "-h", "0.0.0.0"]