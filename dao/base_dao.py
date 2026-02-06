'''
  *** base dao ***
  classe abstrata para data access objects
  operações crud genéricas
'''

from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic
from supabase import Client

# variável de tipo para tornar a classe genérica
T = TypeVar('T')

class BaseDAO(ABC, Generic[T]):

  def __init__(self, client: Client, table_name: str):
    self._client = client
    self._table_name = table_name


  # Do formato JSON (dict) para modelo de dados (T)
  @abstractmethod
  def to_model(self, data: dict) -> T:
    pass

  # Do modelo de dados (T) para formato JSON (dict)
  @abstractmethod
  def to_dict(self, model: T) -> dict:
    pass

  ### Create
  def create(self, model: T) -> Optional[T]:
        """
        cria novo registro no banco de dados

        Args:
            model (T): instãncia do modelo a ser criado

        Returns:
            Optional[T]: instãncia criada com id gerado ou none em caso de erro
        """
        try:
            data = self.to_dict(model)
            response = self._client.table(self._table_name).insert(data).execute()

            if response.data and len(response.data) > 0:
                return self.to_model(response.data[0])
            return None
        except Exception as e:
            print(f"erro ao criar registro: {e}")
            return None

  ### Read
  def read(self, pk: str, value: T) -> Optional[T]:
    try:
      response = self._client.table(self._table_name).select('*').eq(pk, value).execute()
      if response.data and len(response.data) > 0:
        return self.to_model(response.data[0])
      return None
    except Exception as e:
      print(f'erro ao buscar registro: {e}')
      return None

  # retorna todos os registros da tabela
  def read_all(self) -> List[T]:
    try:
      response = self._client.table(self._table_name).select('*').execute()
      if response.data:
        return [self.to_model(item) for item in response.data]
      return []
    except Exception as e:
      print(f'Erro ao buscar todos os registros: {e}')
      return []
    
  ### Update
  def update(self, pk: str, value, model: T) -> Optional[T]:
    """
    Atualiza um registro existente.

    Args:
        pk (str): Nome da coluna chave primária (ex: 'cpf')
        value: Valor da chave primária do registro a atualizar
        model (T): Instância do modelo com os novos dados.

    Returns:
        Optional[T]: Instância atualizada ou None em caso de erro.
    """
    try:
        data = self.to_dict(model)
        
        # remove campos imutáveis e chave primária dos dados
        data.pop(pk, None)
        data.pop('created_at', None)

        response = self._client.table(self._table_name).update(data).eq(pk, value).execute()

        if response.data and len(response.data) > 0:
            return self.to_model(response.data[0])
        return None
    except Exception as e:
        print(f"erro ao atualizar registro: {e}")
        return None

  ### Delete
  def delete(self, pk: str, value) -> bool:
      """
      deleta um registro pela chave primária

      Args:
          pk (str): nome da coluna chave primária (ex: 'cpf')
          value: valor da chave primária do registro a deletar

      Returns:
          bool: true se deletado com sucesso, false caso contrário
      """
      try:
          response = self._client.table(self._table_name).delete().eq(pk, value).execute()
          return True
      except Exception as e:
          print(f"erro ao deletar registro: {e}")
          return False