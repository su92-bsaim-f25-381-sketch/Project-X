from fastapi import FastAPI

app = FastAPI(title="Project X")


@app.get("/")
def home():
    return {
        "project": "Project X",
        "status": "online",
        "mode": "paper_trading"
    }


@app.get("/status")
def status():
    return {
        "bot": "Project X",
        "status": "ready",
        "mode": "paper_trading"
    }