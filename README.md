# Data keeping
Main microservice for datakeeping


## Create development environment Ubuntu

Setup virtual environment

```bash
python3 -m venv env
source env/bin/activate
python3 -m pip install fastapi[all] sqlalchemy
```

Run server for development (reloads when code changes are saved)

```bash
python3 -m uvicorn sql_app.main:app --reload
```