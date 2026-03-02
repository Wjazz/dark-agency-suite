from fastapi import FastAPI
app = FastAPI(title="Founder Risk API")
@app.get("/")
def read_root(): return {"status": "active"}
