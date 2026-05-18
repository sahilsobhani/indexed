from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Welcome to indexed. Refer to our documentation on how to talk to python codebase"}


@app.get("/health")
def health():
    return{ "status": "ok" }
