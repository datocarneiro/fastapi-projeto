from typing import List
from app.models import TarefaCreate, Tarefa  # importando de models as classes TarefaCreate e Tarefa
from datetime import datetime
import pytz

tarefas_db: List[Tarefa] = []
id_counter = 1  # Contador para o campo id (autoincremento)
fuso_horario_brasilia = pytz.timezone('America/Sao_Paulo')

# Função para adicionar uma nova tarefa
def adicionar_tarefa(tarefa: TarefaCreate) -> Tarefa:
    global id_counter
    # Obtendo a data atual com o fuso horário de Brasília
    data_atual = datetime.now(fuso_horario_brasilia)
    
    nova_tarefa = Tarefa(
        id=id_counter,
        titulo=tarefa.titulo,
        descricao=tarefa.descricao,
        status=tarefa.status,
        data_criacao=data_atual,  # Data de criação com timezone
        data_atualizacao=data_atual  # Data de atualização com timezone
    )
    
    tarefas_db.append(nova_tarefa)
    id_counter += 1  # Incrementa o id para a próxima tarefa
    return nova_tarefa

# Função para listar todas as tarefas
def listar_tarefas() -> List[Tarefa]:
    return tarefas_db

# Função para buscar uma tarefa pelo id
def buscar_tarefa_por_id(tarefa_id: int) -> Tarefa:
    for tarefa in tarefas_db:
        if tarefa.id == tarefa_id:
            return tarefa
    return None

# Função para atualizar uma tarefa
def atualizar_tarefa(tarefa_id: int, tarefa: TarefaCreate) -> Tarefa:
    for t in tarefas_db:
        if t.id == tarefa_id:
            t.titulo = tarefa.titulo
            t.descricao = tarefa.descricao
            t.status = tarefa.status
            t.data_atualizacao = datetime.now(fuso_horario_brasilia)
            return t
    return None

# Função para deletar uma tarefa
def deletar_tarefa(tarefa_id: int) -> bool:
    global tarefas_db
    tarefas_db = [t for t in tarefas_db if t.id != tarefa_id]
    return True
