from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def main_page():
    return "Hello There"