import openai
import time
import tiktoken
from dotenv import load_dotenv
import os 
#Constantes
from logging import ERROR #Erro comum  

#Funções
from logging import basicConfig #configurações para os comportamentos dos logs
from logging import error

from logging import getLogger
basicConfig(
    level = ERROR  , #Todas as informações com maior ou prioridade igual ao DEBUG serão armazenadas
    filename= "logs.log", #Onde serão armazenadas as informações 
    filemode= "a", # Permissões do arquivo [se poderá editar, apenas ler ...]
    format= '%(levelname)s->%(asctime)s->%(message)s->%(name)s' # Formatação da informação
)

# Configuração explícita dos loggers das bibliotecas
getLogger('openai').setLevel(ERROR)
getLogger('werkzeug').setLevel(ERROR)

openai.api_key = os.getenv("openai_api_key")
def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def identifica_arquivo(prompt_usuario):
        global prompt_sistema_identifica_arquivo
        prompt_sistema_identifica_arquivo = '''
        # Contexto
    - Você é uma etapa de um chatbot, basicamente o usuário faz uma requisição sobre a cultura do Grupo J&F e o chatbot irá retornar uma resposta. E a função que você está encarregado é retornar o nome de um dos arquivos que mais se relacione com a solicitação do usuário.

    # Missão
    - Sua missão é entender a solicitação do usuário e fazer conexões com os arquivos. É de extrema importância que haja um raciocínio nas conexões porque, ao retornar o nome do arquivo, você estará indicando que este arquivo será suficiente para sanar a solicitação, já que dentro do arquivo se apresenta um resumo do tema citado no título.

    # Instruções
    - É de extrema importância que você retorne apenas o nome do arquivo, porque sua resposta será utilizada num código que irá usar o arquivo, e para que não ocorra nenhum erro, é preciso que só se retorne o nome do arquivo.

    # Arquivos:
    - São  arquivos, abordando os temas dos valores da empresa J&F.
    - Porém tem um arquivo geral com um resumo de todos os valores, muito útil para PERGUNTAS MAIS ABERTAS além de PERGUNTAS QUE SE RELACIONAM com DOIS OU MAIS valores. Segue o nome dos arquivos:

    Humildade.txt;
    AtitudeDeDono.txt;
    Determinacao.txt;
    Disciplina.txt;
    Disponibilidade.txt;
    Franqueza.txt;
    Simplicidade.txt;
    Geral.txt;

    # Exemplo 1
    - Usuário: "Estou com dificuldade de indentificar os valores que me faltam, eu ando muito desanimado porem ainda nao conversei com ninguem para me ajudar."
    - ChatBot: "Geral.txt"
    # Exemplo 2
    - Usuário: "Preciso de ajuda para melhorar minha franqueza. As pessoas reclamam de como abordo elas. Como posso melhorar?"
    - ChatBot: "Franqueza.txt"
    '''

        tentativas = 0
        tempo_de_espera = 5
        try:
            while tentativas <3:
                tentativas+=1
                print(f"Tentativa {tentativas}")
                try:
                    print(f"Iniciando a análise")
                    resposta = openai.ChatCompletion.create(
                        model = "gpt-4-0125-preview",
                        messages = [
                            {
                                "role": "system",
                                "content": prompt_sistema_identifica_arquivo
                            },
                            {
                                "role": "user",
                                "content": prompt_usuario
                            }
                        ],
                        temperature=0.7,
                        max_tokens=100,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                    )
                    
                    print("Análise realizada com sucesso")
                    return "./"+resposta.choices[0].message.content
                except openai.error.AuthenticationError as e:
                    error(e)
                    print(f"Erro de autentificação {e}")
                except openai.error.APIError as e:
                    error(e)
                    print(f"Erro de API {e}")
                    time.sleep(5)
                except openai.error.RateLimitError as e:
                    error(e)
                    print(f"Erro de limite de taxa: {e}")
                    time.sleep(tempo_de_espera)
                    tempo_de_espera *=2
        except Exception as e:
            print('a')
            error(e)
            return e 
    

#
def carrega(nome_do_arquivo):
    try:
        if ('"' in nome_do_arquivo):
            nome_do_arquivo = nome_do_arquivo.replace('"', '')
        with open(nome_do_arquivo, "r", encoding="utf-8") as arquivo:
            
            dados = arquivo.read()
            return dados
    except IOError as e:
        error(e)
        return nome_do_arquivo

#
def respostaApi(prompt_usuario,dadosArquivo, prompt_sistema):
        prompt_sistema = prompt_sistema +'\n# Base De Dados"""' + dadosArquivo + '""""""'
        print(prompt_sistema)
        tentativas = 0
        tempo_de_espera = 5
        try:
            while tentativas <3:
                tentativas+=1
                print(f"Tentativa {tentativas}")
                try:
                    print(f"Iniciando a análise")
                    resposta = openai.ChatCompletion.create(
                        model = "gpt-4-0125-preview",
                        messages = [
                            {
                                "role": "system",
                                "content": prompt_sistema
                            },
                            {
                                "role": "user",
                                "content": prompt_usuario
                            }
                        ],
                        temperature=1,
                        max_tokens=2000,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                    )
                    
                    print("Resposta feita com sucesso")
                    return resposta.choices[0].message.content
                except openai.error.AuthenticationError as e:
                    error('a')
                    print(f"Erro de autentificação {e}")
                except openai.error.APIError as e:
                    error('a')
                    print(f"Erro de API {e}")
                    time.sleep(5)
                except openai.error.RateLimitError as e:
                    print(f"Erro de limite de taxa: {e}")
                    error('a')
                    time.sleep(tempo_de_espera)
                    tempo_de_espera *=2
        except Exception as e:
            error(e)
            return e 
    
#######     
