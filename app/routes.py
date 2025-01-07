from fastapi import APIRouter, HTTPException
from app.db import adicionar_tarefa, listar_tarefas, buscar_tarefa_por_id, atualizar_tarefa, deletar_tarefa
from app.models import TarefaCreate, Tarefa

router = APIRouter()

# Endpoint para criar uma tarefa
@router.post("/tarefas/", response_model=Tarefa)
def criar_tarefa(tarefa: TarefaCreate):
        # Validar o status da tarefa
        if tarefa.status not in ["pendente", "em andamento", "concluída"]:
            raise HTTPException(status_code=400, detail="status inválido")
        return adicionar_tarefa(tarefa)


# Endpoint para listar todas as tarefas
@router.get("/tarefas/", response_model=list[Tarefa])
def get_tarefas():
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
