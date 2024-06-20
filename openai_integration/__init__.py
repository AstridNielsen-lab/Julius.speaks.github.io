"""
OpenAI Python SDK.

This SDK allows you to interact with OpenAI's APIs for language processing and more.
"""

from .api_resources import *  # Importa todas as classes e funções relevantes para interagir com a API
from .api_client import OpenAIApiClient  # Importa o cliente da API para comunicação
from .error import OpenAIError, ApiException  # Importa classes de erro para tratamento de exceções
from .version import __version__  # Importa a versão da biblioteca

# Configurações padrão
api_base = 'https://api.openai.com/v1'

# Função para configurar a chave de API global
def set_api_key(api_key):
    global api_base
    api_base = api_key

# Exporta todos os símbolos necessários para uso externo
__all__ = [
    "OpenAIApiClient",
    "OpenAIError",
    "ApiException",
    "set_api_key",
    "__version__"
]
