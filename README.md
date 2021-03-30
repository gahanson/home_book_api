# Home Book API  
### note: THIS PROJECT IS A WORK INPROGRESS
- REST api to organize, catalog local epub and pdf files

### technologies used  
  
 - Django 3  
 - django rest framework    
 - psycopg2 to connect to postgresql database  
 - python-dotenv for environment variables (.env file)  
 - python venv environment for development  
 - docker for deployment   

**require .env file in project root in the following format**  
DJANGO_SECRET=  
DATABASE_NAME=  
DATABASE_USER=  
DATABASE_PASSWORD=  
DATABASE_HOST_IP=  
DATABASE_PORT=  
CORS_ALLOWED_LIST=  
ADMIN_USER_NAME=  
ADMIN_USER_EMAIL=  
ADMIN_USER_PASSWORD=  

**required postgresql database running on the local network with a database already created**


## Endpoints  

**GET bookapi/book/**  
- return json of all books in database, corresponds to all books on file system  
- id, local_path, remote_url, viewer_path  
- search allowed, bookapi/book/?search=  

**POST bookapi/book/**  
- write book data to database  
- local_path, remote_url, viewer_path  

**GET bookapi/availablebook/**  
- return json of all books available to view in a web browser,corresponds to books that have been processed manually by user  
- id, title, author, book  
- search allowed, bookapi/availablebook/?search=  

**POST bookapi/availablebook/**  
- write book data to database  
- title, author, book_id  

**GET songapi/settings/**  
- read all user settings  
- id, source_ip, source_script_path, source_viewer_base_url  

**POST songapi/settings/**  
- write user settings to database  
- source_ip, source_script_path, source_viewer_base_url

**PUT songapi/refresh/**  
- return json of both, book files added to database, and deleted from database  
- when files are added to or deleted from the local harddrive the refresh  
endpoint will update the database to reflect the files in the directory path