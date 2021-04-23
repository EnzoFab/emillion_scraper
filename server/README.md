# Server

Server using FastAPI. provides the reworked resources gathered by the webscraping process.

## init

First install all the dependencies listed in the *requirements* file

```bash
pip install -r requirements.txt
```

## start

### dev

To start the server in dev mode

```bash
uvicorn main:app --reload
```

The server: http://127.0.0.1:8000/

The swagger: http://127.0.0.1:8000/docs