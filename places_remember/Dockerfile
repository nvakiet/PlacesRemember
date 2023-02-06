# Stage 0
FROM python:3.9.16 as requirement_installer
# Install dependencies to prefix directory
COPY requirements.txt .
RUN pip install --prefix=/required_packages -r requirements.txt --no-cache-dir

# Stage 1
FROM python:3.9.16-slim
WORKDIR /code
# Install runtime dependencies for psycopg2 package
RUN apt-get update && apt-get -y install libpq-dev
RUN apt-get clean
# Move installed binaries to runtime image
COPY --from=requirement_installer /required_packages /usr/local
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Copy source contents
COPY . /code/

# Run the Django app setup script on startup
RUN chmod -R 777 /code/docker-entrypoint.sh
ENTRYPOINT [ "/code/docker-entrypoint.sh" ]