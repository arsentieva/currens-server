#  Initial application setup
pipenv install Flask~=1.1


# create  and open a file
currens.py

# import flask in to the file created
Initialize the app using the __name__ dunder.

# To ease the usage of environment variables, install python-dotenv
pipenv install python-dotenv~=0.13

# Create and set up your .flaskenv (FLASK_APP=currens.py) and .env (SECRET_KEY=<<key>> and FLASK_ENV=development)

# Create config file to expose env variables
app.config.from_object(Config)


##### Database setup
# installing Psycopg2, SQLAlchemy, and Flask-SQLAlchemy
pipenv install --python "$PYENV_ROOT/shims/python" Flask psycopg2-binary \
SQLAlchemy Flask-SQLAlchemy

### once models are complete it is time to migrate
1. initialize the local Alembic
  ``` pipenv run flask db init ```

2. create migration file
    ``` pipenv run flask db migrate -m "create currens tables" ```

3. run migration file
    ``` pipenv run flask db upgrade ```
