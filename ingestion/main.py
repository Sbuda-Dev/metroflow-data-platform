from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():

    return {"message": "MetroFlow Data Platform"}