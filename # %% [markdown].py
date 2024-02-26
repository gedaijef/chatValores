import os
import openai
import dotenv
import time
openai.api_key = "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"
import tiktoken

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def identificaArquivo(prompt_usuario):
    try:
        global prompt_sistema_identificaArquivo
        prompt_sistema_identificaArquivo = '''
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
                            "content": prompt_sistema_identificaArquivo
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
                return "C:/Users/arthurdomingos-ieg/OneDrive - Instituto Germinare/Área de Trabalho/GEDAI/projetoValores/Dados/"+resposta.choices[0].message.content
            except openai.error.AuthenticationError as e:
                print(f"Erro de autentificação {e}")
            except openai.error.APIError as e:
                print(f"Erro de API {e}")
                time.sleep(5)
            except openai.error.RateLimitError as e:
                print(f"Erro de limite de taxa: {e}")
                time.sleep(tempo_de_espera)
                tempo_de_espera *=2
    except:
        print("ERROR")
        



#
def carrega(nome_do_arquivo):
    try:
        if ('"' in nome_do_arquivo):
            nome_do_arquivo = nome_do_arquivo.replace('"', '')
        with open(nome_do_arquivo, "r", encoding="utf-8") as arquivo:
            
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro no carregamento de arquivo: {e}")
        return nome_do_arquivo

#
def respostaApi(prompt_usuario,dadosArquivo, prompt_sistema):   
    prompt_sistema = prompt_sistema +'\n# Base De Dados"""' + dadosArquivo + '""""""'
    print(prompt_sistema)
    tentativas = 0
    tempo_de_espera = 5
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
            print(f"Erro de autentificação {e}")
        except openai.error.APIError as e:
            print(f"Erro de API {e}")
            time.sleep(5)
        except openai.error.RateLimitError as e:
            print(f"Erro de limite de taxa: {e}")
            time.sleep(tempo_de_espera)
            tempo_de_espera *=2




#######
         

prompt_sistema_respostaApi = f'''
    # Contexto

- Você é um chatbot especializado na cultura do Grupo J&F, possuindo amplo conhecimento sobre seus valores, missões, crenças, entre outros. Seu linguajar é natural e apropriado.

# Missão

- Sua missão é compreender as solicitações do usuário e fornecer respostas que agreguem valor, esclareçam dúvidas ou respondam a afirmações de maneira construtiva.

# Instruções

- A FORMATAÇÃO DA RESPOSTA DEVE SER EM LISTA E SUB-LISTAS
- Compreenda detalhadamente a solicitação do usuário, associe-a à cultura do Grupo J&F. Seja claro na resposta e evite usar muitos tokens. Aborde esta tarefa metodicamente, sem pressa e sem pular etapas.
- RESPONDA SOMENTE SE ESTIVER RELACIONADO A ISSO. Qualquer outra solicitação será respondida com esta mensagem que explica o porquê de não poder esclarecer.MENSAGEM: "Por favor insira mais detalhes de sua solicitação por conta que"[COMPLEMENTE COM O PORQUE DO NÃO PODER RESPONDER].

# Exemplo

- Usuário: "meu colega me excluiu de um trabalho em grupo, no que ele deve melhorar e o que devo falar para ele?"
- ChatBot: "🔍 Para Melhorar: Seu colega pode focar em:

Trabalho em Equipe 🤝: Reconhecer a importância de incluir todos e trabalhar juntos, respeitando a contribuição de cada um.
Compromisso com o Grupo 🌟: Entender que o sucesso do grupo depende da participação e colaboração de todos.
🗣️ O que Dizer:

Expresse Seus Sentimentos 💬: Diga como se sentiu excluído e a importância de trabalhar juntos.
Valores do Instituto Germinare 🏫: Lembre-o de que a atitude de dono inclui comprometimento com o grupo e colaboração.
Crescimento Conjunto 📈: Enfatize que todos no grupo têm algo valioso a contribuir para o sucesso coletivo.
Espero que isso ajude a melhorar a dinâmica do grupo! 🌟"

#Base De Dados
"""
'''


# Segunda parte, HISTORICO

#Variavieis globais   
variavelGlobal = 0
listaHistorico = ["","",""]


from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

@app.route('/')

def index():
    return render_template('index.html')

#Todo projeto será acionado no submite do usuario
@app.route('/submit',methods = ['POST'])


def submit():
    try:
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("0")
        global variavelGlobal
        global prompt_sistema_respostaApi
        global listaHistorico
        if(variavelGlobal == 0):
            variavel = request.form['inputMessage']

            print(variavel)
            #Api GPT
            variavel = variavel+" Além de tudo isso, para tornar a mensagem mais interativa, insira emojis relacionados com a sua resposta."
            respostaIdentificaArquivo = identificaArquivo(variavel)

            dadosArquivo = carrega(respostaIdentificaArquivo)

            resposta = respostaApi(variavel,dadosArquivo,prompt_sistema_respostaApi)
            variavelGlobal=variavelGlobal+1
            listaHistorico[variavelGlobal] = f"""#CONVERSA ANTERIOR {variavelGlobal}
    -Solicitação anterior do usuário:
    {variavel}
    -Resposta anterior:
    {resposta}
    """
            prompt_sistema_respostaApi = f'''
        # Contexto

        - Você é um chatbot especializado na cultura do Grupo J&F, possuindo amplo conhecimento sobre seus valores, missões, crenças, entre outros. Seu linguajar é natural e apropriado.
        - Você está aqui porque foi solicitado pelo usuário a ativação do histórico do chat. Assim, você possui todas as informações necessárias das últimas conversas e sobre a nova solicitação do usuário. Você deve fazer uma resposta embasada nas últimas informações da conversa.

        # Missão

        - Sua missão é compreender as solicitações do usuário e fornecer respostas que agreguem valor, esclareçam dúvidas ou respondam a afirmações de maneira construtiva.

        # Instruções

        - A FORMATAÇÃO DA RESPOSTA DEVE SER EM LISTA E SUB-LISTAS
        - Compreenda detalhadamente a solicitação do usuário, associe-a à cultura do Grupo J&F e RESPONDA SOMENTE SE ESTIVER RELACIONADO A ISSO. Qualquer outra solicitação será respondida com uma mensagem explicando o porquê de não poder esclarecer ou se achar que a resposta apenas precisa de mais detalhes, peça para o usuario dar mais informações sobre sua solicitação. SEJA CLARO NA RESPOSTA E EVITE USAR MUITOS TOKENS. Aborde esta tarefa metodicamente, sem pressa e sem pular etapas.
        - Além disso, para tornar a mensagem mais interativa, insira EMOJIS relacionados à sua resposta.
        '''
            #Api GPT
            # Passa a variável para o template HTML
            # return render_template('index.html', variavel_frontend=resposta)
            return jsonify({'resposta': resposta})
        elif(variavelGlobal == 1):
            print("1")

            variavel = request.form['inputMessage']

            print(variavel)
            #Api GPT
            variavel = variavel+" Além de tudo isso, para tornar a mensagem mais interativa, insira emojis relacionados com a sua resposta."
            respostaIdentificaArquivo = identificaArquivo(variavel)

            dadosArquivo = carrega(respostaIdentificaArquivo)

            # prompt_sistema_respostaApi += listaHistorico[variavelGlobal] + listaHistorico[variavelGlobal+1]

            resposta = respostaApi(variavel,dadosArquivo,prompt_sistema_respostaApi+listaHistorico[variavelGlobal] + listaHistorico[variavelGlobal+1])
            variavelGlobal = variavelGlobal+1
            listaHistorico[variavelGlobal] = f'''#CONVERSA ANTERIOR {variavelGlobal}
    -Solicitação anterior do usuário:
    {variavel}
    -SUA RESPOSTA PARA A SOLICITAÇÃO:
    {resposta}
    """
    '''
            #Api GPT
            # Passa a variável para o template HTML
            # return render_template('index.html', variavel_frontend=resposta)
            return jsonify({'resposta': resposta})

        else:
            print("2")

            variavel = request.form['inputMessage']

            print(variavel)
            #Api GPT
            variavel = variavel+" Além de tudo isso, para tornar a mensagem mais interativa, insira emojis relacionados com a sua resposta."
            respostaIdentificaArquivo = identificaArquivo(variavel)
            
            dadosArquivo = carrega(respostaIdentificaArquivo)
            
            resposta = respostaApi(variavel,dadosArquivo,prompt_sistema_respostaApi+listaHistorico[variavelGlobal] + listaHistorico[variavelGlobal-1])
            variavelGlobal = variavelGlobal-1
            listaHistorico[variavelGlobal] = f'''#CONVERSA ANTERIOR {variavelGlobal}
    -Solicitação anterior do usuário:
    {variavel}
    -Resposta anterior:
    {resposta}
    """
    '''
            #Api GPT
            # Passa a variável para o template HTML
            # return render_template('index.html', variavel_frontend=resposta)
            return jsonify({'resposta': resposta})

    except:
        return render_template('index.html', variavel_frontend="ERROR")

app.run(debug=True)


