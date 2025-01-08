from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.db import adicionar_tarefa, listar_tarefas, buscar_tarefa_por_id, atualizar_tarefa, deletar_tarefa
from app.auth import authenticate_user, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES, fake_users_db
from app.models import TarefaCreate, Tarefa
from pydantic import BaseModel
from datetime import datetime, timedelta

router = APIRouter()

# Endpoint para criar uma tarefa
@router.post("/tarefas/", response_model=Tarefa)
def criar_tarefa(tarefa: TarefaCreate, current_user: dict = Depends(get_current_user)):
        # Validar o status da tarefa
        if tarefa.status not in ["pendente", "em andamento", "concluída"]:
            raise HTTPException(status_code=400, detail="status inválido")
        return adicionar_tarefa(tarefa)


# Endpoint para listar todas as tarefas
@router.get("/tarefas/", response_model=list[Tarefa])
def get_tarefas(current_user: dict = Depends(get_current_user)):
    return listar_tarefas()

# Endpoint para buscar uma tarefa pelo id
@router.get("/tarefas/{id_tarefa}", response_model=Tarefa)
def get_tarefa(id_tarefa: int):
    tarefa = buscar_tarefa_por_id(id_tarefa)
    if tarefa is None:
        raise HTTPException(status_code=404, detail = f"Tarefa ID:{id_tarefa} não encontrada")
    return tarefa

# Endpoint para atualizar uma tarefa
@router.put("/tarefas/{id_tarefa}", response_model=Tarefa)
def update_tarefa(id_tarefa: int, tarefa: TarefaCreate):
    updated_tarefa = atualizar_tarefa(id_tarefa, tarefa)
    if updated_tarefa is None:
        raise HTTPException(status_code=404, detail = f"Tarefa ID:{id_tarefa} não encontrada")
    return updated_tarefa

# Endpoint para deletar uma tarefa
@router.delete("/tarefas/{id_tarefa}", response_model=dict)
def delete_tarefa(id_tarefa: int):
    if deletar_tarefa(id_tarefa):
        return {'msg': f'Tarefa com ID:{id_tarefa} deletada com sucesso!'}
    raise HTTPException(status_code=404, detail= f"Tarefa ID:{id_tarefa} não encontrada")

class LoginInput(BaseModel):
    username: str
    password: str

@router.post("/auth/login")
def login(login_data: LoginInput):
    user = authenticate_user(fake_users_db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint protegido (exemplo)
@router.get("/tarefas/protegido")
def read_protected_tarefas(current_user: dict = Depends(get_current_user)):
    return {"msg": f"Bem-vindo, {current_user['username']}! Você está autenticado."}
