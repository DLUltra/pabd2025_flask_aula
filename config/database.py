# módulo de conexão com supabase
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# carregando variáveis de ambiente
load_dotenv()

class SupabaseConnection:
  '''
  padrão singleton para garantir uma única instãncia
  '''
  _instance = None
  # type hint - garante o tipo de dado
  _client: Client = None

  # cria instância da classe
  def __new__(cls):
    if cls._instance is None:
      cls._instance = super(SupabaseConnection, cls).__new__(cls)
      cls._instance._init_connection()
    return cls._instance
  
  def _init_connection(self):
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')

    if not supabase_url or not supabase_key:
      raise ValueError('erro nas variáveis de ambiente ✅')

    self._client = create_client(supabase_url, supabase_key)
    print('conexão com supabase estabelecida ✅')

  @property
  def client(self) -> Client: # type hint
    return self._client