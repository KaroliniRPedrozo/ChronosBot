from fastapi import FastAPI
from App.database import engine, Base
from App.api import admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ChronosBot API")

# Inclui as rotas do admin
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

@app.get("/")
def home():
    return {"message": "ChronosBot API ativa e pronta para TCC!"}