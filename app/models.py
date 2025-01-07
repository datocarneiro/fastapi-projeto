from pydantic import BaseModel, Field, root_validator
from typing import Optional
from datetime import datetime
import pytz

# Fuso horário de Brasília
fuso_horario_brasilia = pytz.timezone('America/Sao_Paulo')

# Modelo base para a tarefa
class TarefaBase(BaseModel):
    titulo: str  # Campo obrigatório
    descricao: Optional[str] = None  # Campo opcional
    estado: str  # Campo obrigatório
    data_criacao: datetime = Field(default_factory=lambda: datetime.now(fuso_horario_brasilia))  # Data de criação gerada automaticamente com timezone
    data_atualizacao: datetime = Field(default_factory=lambda: datetime.now(fuso_horario_brasilia))  # Data de atualização gerada automaticamente com timezone

    # Validação para o campo 'estado'
    @root_validator(pre=True)
    def validar_estado(cls, values):
        estado = values.get('estado')
        estados_validos = ["pendente", "em andamento", "concluída"]
        if estado and estado not in estados_validos:
            raise ValueError(f"Estado '{estado}' não é válido. \nOs estados validos são: {estados_validos}.")
        return values

    class Config:
        orm_mode = True  # Permite conversão automática entre Pydantic e ORM

# Modelo para criação de tarefa (sem o id, pois o id será autoincrementado)
class TarefaCreate(TarefaBase):
    pass

# Modelo para representar a tarefa completa (inclui o id autoincrementado)
class Tarefa(TarefaBase):
    id: int  # Campo id autoincrementado
