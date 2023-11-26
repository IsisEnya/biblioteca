FROM python:3.11.6

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt -v



COPY . /app
RUN python manage.py collectstatic --no-input

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]