from fastapi import APIRouter, HTTPException
from app.db import adicionar_tarefa, listar_tarefas, buscar_tarefa_por_id, atualizar_tarefa, deletar_tarefa
from app.models import TarefaCreate, Tarefa

router = APIRouter()

# Endpoint para criar uma tarefa
@router.post("/tarefas/", response_model=Tarefa)
def criar_tarefa(tarefa: TarefaCreate):
    # Validar o estado da tarefa
    if tarefa.estado not in ["pendente", "em andamento", "concluída"]:
        raise HTTPException(status_code=400, detail="Estado inválido")
    return adicionar_tarefa(tarefa)

# Endpoint para listar todas as tarefas
@router.get("/tarefas/", response_model=list[Tarefa])
def get_tarefas():
    return listar_tarefas()

# Endpoint para buscar uma tarefa pelo id
@router.get("/tarefas/{tarefa_id}", response_model=Tarefa)
def get_tarefa(tarefa_id: int):
    tarefa = buscar_tarefa_por_id(tarefa_id)
    if tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa

# Endpoint para atualizar uma tarefa
@router.put("/tarefas/{tarefa_id}", response_model=Tarefa)
def update_tarefa(tarefa_id: int, tarefa: TarefaCreate):
    updated_tarefa = atualizar_tarefa(tarefa_id, tarefa)
    if updated_tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return updated_tarefa

# Endpoint para deletar uma tarefa
@router.delete("/tarefas/{tarefa_id}", response_model=dict)
def delete_tarefa(tarefa_id: int):
    if deletar_tarefa(tarefa_id):
        return {"msg": "Tarefa deletada com sucesso!"}
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")
