from datetime import datetime
from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator


class GerarSimuladoInput(BaseModel):
    turma_id: int
    titulo: str = Field(min_length=2, max_length=255)
    numero_questoes: int = Field(default=5, ge=1, le=20)


class QuestaoGeradaIA(BaseModel):
    """
    Schema estrito usado para validar a saída JSON do Gemini.
    Se a validação falhar, o serviço de geração faz retry (ver
    services/simulado_service.py) com o erro devolvido ao modelo.
    """
    enunciado: str = Field(min_length=5)
    alternativas: Dict[Literal["A", "B", "C", "D"], str]
    resposta_correta: Literal["A", "B", "C", "D"]
    explicacao: str = Field(min_length=3)

    @field_validator("alternativas")
    @classmethod
    def validar_quatro_alternativas(cls, v):
        if set(v.keys()) != {"A", "B", "C", "D"}:
            raise ValueError("É necessário fornecer exatamente as alternativas A, B, C e D.")
        return v


class SimuladoGeradoIA(BaseModel):
    """Envelope da resposta completa esperada do Gemini para um simulado."""
    questoes: List[QuestaoGeradaIA]


class QuestaoSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ordem: int
    enunciado: str
    alternativas: Dict[str, str]
    # resposta_correta e explicacao são omitidos aqui de propósito ao entregar
    # o simulado ao aluno antes da correção — ver QuestaoComGabaritoSaida.


class QuestaoComGabaritoSaida(QuestaoSaida):
    resposta_correta: str
    explicacao: Optional[str] = None


class SimuladoSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    turma_id: int
    criado_em: datetime
    questoes: List[QuestaoSaida]


class ResponderSimuladoInput(BaseModel):
    respostas: Dict[int, Literal["A", "B", "C", "D"]]  # {questao_id: resposta}


class TentativaSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    simulado_id: int
    nota: float
    finalizado_em: datetime
    questoes_com_gabarito: List[QuestaoComGabaritoSaida] = []
