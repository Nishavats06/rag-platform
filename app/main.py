from fastapi import FastAPI

app = FastAPI(title="Document Search & RAG Platform")


@app.get("/health/live")
def live():
    return {"success": True, "message": "alive", "data": {"status": "ok"}}