# Places Remember
This is a simple website for keeping notes about places you have visited. The website uses Facebook for user authentication and Google Map to assist with finding place addresses.  

I made this website to practice web development using a basic web stack of: Django, Uvicorn/Gunicorn, Nginx and Docker.  

**Demo video:**  [https://youtu.be/eAZiFpQVDHQ](https://youtu.be/eAZiFpQVDHQ)

## 1. Setup
Simply clone this repository (or use the sources in Release) to start using it.  
### a. SSL certificate
The web app has been configured to run on HTTPS protocol due to Facebook API requirement so you need an SSL certificate. If you already have a domain name for your public IP (such as [NoIP](https://www.noip.com/) domains), you can use [Let's Encrypt](https://letsencrypt.org/) + [Certbot](https://certbot.eff.org/) to get free SSL certification for your domain. If you want to run on a local development environment (i.e localhost), you can use [mkcert](https://github.com/FiloSottile/mkcert) to make a self-signed certification.  

Once you have your SSL certificate and key `*.pem` files, place them in a subfolder in the project `certs` folder. The repository already has a `certs/localhost` folder for placing localhost SSL certificate and key.  

### b. Create Facebook and Google API keys  
To run the web server, you need to create your own API keys and put them in the `.env` file.  

For the Facebook API key, enable the Facebook Login product.  
For the Google API key, enable the Google Map Javascript API, Map Embed API, Places API and Geocoding API.  

**Warning:** To use the Google Map API, the API key needs to be embedded on the html script tag to import the libraries, so the API key will be exposed on the client side. I tried to find ways to import the libraries without exposing the key but haven't found one yet. The Google Map API documentations only says to set restriction on the API keys. So make sure that the Google API key used in this project is restricted to the project's web domain, only allow the key for the Google Map Javascript API, Embed Map API, Places API and Geocoding API. For good measures, also set the API quota properly to prevent the user from overusing the API since there isn't a cache for the Google API calls yet.  

### c. Set environment variables  
The project will read some of its settings and sensitive information from the environment variables. You must create your own `.env` file in the project root. Here's a sample template for reference:  

```bash
# For Django settings
export DJANGO_SECRET_KEY=Your_Generated_Django_Secret_Key
export DJANGO_DB_HOST=postgres
export DJANGO_DB_PORT=5432
export TIME_ZONE=Asia/Ho_Chi_Minh

# Postgres database settings
export POSTGRES_NAME=postgres
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=Your_PostGres_Password

# For Facebook authentication API
# Facebook App ID
export SOCIAL_AUTH_FACEBOOK_KEY=Your_Facebook_App_ID
# Facebook App Secret
export SOCIAL_AUTH_FACEBOOK_SECRET=Your_Facebook_App_Secret

# For Google Map API
# Google Map Javascript API, Map Embed API, Places API, Geocoding API
export GOOGLE_API_KEY=Your_API_Key

# Nginx configuration
export NGINX_HOST=localhost # Or your web hosting domain
# SSL certificate and key must be in a subfolder of the certs folder
export SSL_KEY_PATH=/certs/localhost/key.pem 
export SSL_CERT_PATH=/certs/localhost/cert.pem

# Deployment settings
# DEV for development mode, PROD for production mode
export DEPLOY_MODE=DEV
# Based on number of CPU cores, per Uvicorn/Gunicorn documentation
export N_UVICORN_WORKERS=4
```   

### d. Nginx configurations  
Nginx is used here to reverse proxy and cache proxy responses for HTTPS. You can tinker with the Nginx configurations if needed. The configuration files are placed in the `nginx_templates` folder. Within that folder, the `nginx.conf` and `default.conf.template` are for overriding the default configurations within the Nginx container for easier debugging during development without having to tap into the container terminal. The main configurations are in `nginx.conf.template`.

Also since the `media` folder is ignored when pushing to git. You should create one at the project root for the Nginx container to bind a volume to in case the container doesn't create it automatically.

Read the [Nginx Docker Guide](https://hub.docker.com/_/nginx) for more details on how the configuration template works.

## 2. Unit testing
In the Django server, there are unit tests for the "User memories" page and "Add memory" page. These are tests to be run in development mode. I have created some test data fixture in `place_memories/fixtures`. Simply use the Django management command to run the tests.  

```bash
# set DEPLOY_MODE=DEV in the .env file
# Run the docker compose
docker compose up -d
# Go to the container terminal of the webapp then run
python manage.py test
```

Or if you want to run the tests outside of the docker terminal:

```bash
# set DEPLOY_MODE=DEV 
# set DJANGO_DB_HOST=localhost
# Run only the database container
docker compose up -d postgres adminer
# Then run the tests from outside of docker
cd places_remember
python manage.py test
```

## 3. Running the server  
All components of the web application are contained inside Docker containers. Simply run the whole stack using Docker Compose from the project root:  

```
docker compose up -d
```

To stop it:  
```
docker compose down
```

You can change between running in development or production mode by setting the `DEPLOY_MODE` variable in the `.env` file.

## 3. Features  
For now, there are only some basic features, I will keep adding to this project when I have the time (and feel like doing it...):  
- Login/Logout with Facebook authentication;  
- Create new place memory;
- View list of memories;  
- Show Google Map for selecting a location when adding new memory;  
- Address suggestion when adding new memory;   

To-do (This is just for my own learning when I have the time):   
- Add other CRUD features, such as: deleting and editing memories;  
- Learn and use a more sophisticated front-end framework, such as Vue.js;  
- Set up a dedicated cache database like Redis;  
- Use template inheritance for reusable template parts;  
- Host the website, either with cloud service or self-hosting;
- Find a way to not expose the Google API key;
