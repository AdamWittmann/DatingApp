# Semester Project Template

## set up
### virtual environment
1. install virtualenv virtual environment
    ```bash
    pip install virtualenv
    # or
    python3 -m pip install virtualenv
    ```
2. create a virtual environment
    ```bash
    # create venv
    virtualenv .venv
    # or 
    python3 -m virtualenv .venv
   ```

2. activate the virtual environment
    ```bash
    pip install virtualenv
    # or
    python3 -m pip install virtualenv
    ```
4. install the project dependencies
     ```bash
    pip install -r requirements.txt
    # or
    python3 -m pip install -r requirements.txt
    ```

### postgresql
1. install postgres version 16.4: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

2. create a database

3. create a .env file in the project root

4. add the following values to the .env file
    ```bash
    db_name = <db name>
    db_owner = postgres
    db_pass = <db pass>
    ```



## project layout

### db package
- server.py: connects to database & creates flask application
- schema: stores database tables defined by python classes

### static
- style.css: external stylesheet
- images: stores images

### templates
- stores html documents that represent webpages
- index.html: example webpage

### app.py
- renders html templates

## running the application
    
run the flask application with 
```bash
python app.py
# or
python3 app.py
```
