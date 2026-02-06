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
    """retorna o datetime atual no fuso horário de são paulo"""
    tz_br = timezone(timedelta(hours=-3))  # UTC-3 (Brasília)
    return datetime.now(tz_br).replace(tzinfo=None)

  # sobrescreve método create para adicionar created_at automaticamente
  def create(self, model: Funcionario) -> Optional[Funcionario]:
    """cria um novo funcionário com data de criação automática"""
    model._created_at = self._get_datetime_br()
    return super().create(model)

  # sobrescreve método update para adicionar updated_at automaticamente
  def update(self, pk: str, value, model: Funcionario) -> Optional[Funcionario]:
    """atualiza um funcionário com data de atualização automática"""
    model._updated_at = self._get_datetime_br()
    return super().update(pk, value, model)

  # métodos específicos para funcionário (usando cpf como chave primária)
  def read_by_cpf(self, cpf: str) -> Optional[Funcionario]:
    """busca um funcionário pelo cpf"""
    return self.read('cpf', cpf)

  def update_by_cpf(self, cpf: str, funcionario: Funcionario) -> Optional[Funcionario]:
    """atualiza um funcionário pelo cpf"""
    return self.update('cpf', cpf, funcionario)

  def delete_by_cpf(self, cpf: str) -> bool:
    """deleta um funcionário pelo cpf"""
    return self.delete('cpf', cpf)