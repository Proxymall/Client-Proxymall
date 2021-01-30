FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip3 install fastapi uvicorn sqlalchemy peewee python-jose[cryptography] passlib[bcrypt] fastapi-login
EXPOSE 80
COPY ./app /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80" ]
