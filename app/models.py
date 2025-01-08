from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import pytz

# Fuso horário de Brasília
fuso_horario_brasilia = pytz.timezone('America/Sao_Paulo')

# Modelo base para a tarefa
class TarefaBase(BaseModel):
    titulo: str  # Campo obrigatório
    descricao: Optional[str] = None  # Campo opcional
    status: str  # Campo obrigatório
    data_criacao: datetime = Field(default_factory=lambda: datetime.now(fuso_horario_brasilia))  # Data de criação gerada automaticamente com timezone
    data_atualizacao: datetime = Field(default_factory=lambda: datetime.now(fuso_horario_brasilia))  # Data de atualização gerada automaticamente com timezone
    
    # Validação para o campo 'status'
    @field_validator('status')
    def validar_status(cls, status):
        status_validos = ["pendente", "em andamento", "concluída"]
        if status not in status_validos:
            raise ValueError(f"status '{status}' não é válido. Os status válidos são: {status_validos}.")
        return status

    class Config:
        from_attributes = True  # Permite conversão automática entre Pydantic e ORM

# Modelo para criação de tarefa (sem o id, pois o id será autoincrementado)
class TarefaCreate(TarefaBase):
    pass

# Modelo para representar a tarefa completa (inclui o id autoincrementado)
class Tarefa(TarefaBase):
    id: int  # Campo id autoincrementado


