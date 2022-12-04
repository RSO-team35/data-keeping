# Data keeping
Main microservice for datakeeping


#### Local setup


Run server for development (reloads when code changes are saved)

```bash
python3 -m uvicorn sql_app.main:app --reload
```

Access OpenAPI docs at:

http://127.0.0.1:8000/docs#/