from fastapi import FastAPI

app = FastAPI(title="MotherCare 360")


@app.get("/")
def home():
    return {
        "message": "MotherCare 360 Backend is running"
    }