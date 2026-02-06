from typing import Optional
from datetime import datetime, timezone, timedelta
from supabase import Client
from dao.base_dao import BaseDAO
from models.funcionario import Funcionario

class FuncionarioDAO(BaseDAO[Funcionario]):

  def __init__(self, client: Client):
    super().__init__(client, 'funcionario')

  def to_model(self, data: dict) -> Funcionario:
    return Funcionario.from_dict(data)

  def to_dict(self, model: Funcionario) -> dict:
    return model.to_dict()

  # Função auxiliar para obter horário brasileiro
  def _get_datetime_br(self):
    """Retorna o datetime atual no fuso horário de São Paulo"""
    tz_br = timezone(timedelta(hours=-3))  # UTC-3 (Brasília)
    return datetime.now(tz_br).replace(tzinfo=None)

  # Override create para adicionar created_at automaticamente
  def create(self, model: Funcionario) -> Optional[Funcionario]:
    """Cria um novo funcionário com data de criação automaticamente"""
    model._created_at = self._get_datetime_br()
    return super().create(model)

  # Override update para adicionar updated_at automaticamente
  def update(self, pk: str, value, model: Funcionario) -> Optional[Funcionario]:
    """Atualiza um funcionário com data de atualização automaticamente"""
    model._updated_at = self._get_datetime_br()
    return super().update(pk, value, model)

  # Métodos específicos para Funcionario (usando CPF como chave primária)
  def read_by_cpf(self, cpf: str) -> Optional[Funcionario]:
    """Busca um funcionário pelo CPF"""
    return self.read('cpf', cpf)

  def update_by_cpf(self, cpf: str, funcionario: Funcionario) -> Optional[Funcionario]:
    """Atualiza um funcionário pelo CPF"""
    return self.update('cpf', cpf, funcionario)

  def delete_by_cpf(self, cpf: str) -> bool:
    """Deleta um funcionário pelo CPF"""
    return self.delete('cpf', cpf)