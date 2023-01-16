# PlacesRemember
Saritasa's Python Developer Intern Test   
To run the web server with Docker, first create a `.env` file in the repository root. Inside the file, specify the environment variables as the following examples:   
```
export DJANGO_SECRET_KEY=Your_Django_Secret_Key
export POSTGRES_NAME=postgres
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=yourDbPasswordHere
export DJANGO_DB_HOST=localhostOrDbContainerName
export DJANGO_DB_PORT=5432 # Do not recommend to change this number
export TIME_ZONE=Asia/Ho_Chi_Minh # If not specified, the app will use UTC
```   
