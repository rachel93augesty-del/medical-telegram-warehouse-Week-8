from fastapi import FastAPI
from api.routers import reports, channels, search

app = FastAPI(title="Medical Telegram Analytics API", version="0.1.0")

app.include_router(reports.router)
app.include_router(channels.router)
app.include_router(search.router)
