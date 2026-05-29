from fastapi import FastAPI
from sqlalchemy import text

from .database import engine, get_db
from .endpoints import analytics, utils
from .core.logger import setup_logging


app = FastAPI(title="Safe Analytics Query Service Assessment", version="1.0.0")

setup_logging()

app.include_router(analytics.router, tags=["analytics"])
app.include_router(utils.router, tags=["utils"])


@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/ready")
async def readiness_check():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            return {"status": "ready"}
    except Exception as e:
        return {"status": "not ready", "error": str(e)}

