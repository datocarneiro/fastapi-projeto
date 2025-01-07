from fastapi import FastAPI
from app.routes import router as tarefa_router

app = FastAPI()

# Incluir os endpoints no FastAPI
app.include_router(tarefa_router)

@app.get("/")
def read_root():
    return {"message": "API de gerenciamento de tarefas - PIXAFLOW"}
