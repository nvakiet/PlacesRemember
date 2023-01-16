FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt --no-cache-dir
COPY . /code/

# Run the Django app setup script on startup
RUN chmod -R 777 /code/docker-entrypoint.sh
ENTRYPOINT [ "/code/docker-entrypoint.sh" ]