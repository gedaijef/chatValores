import funcoes_OpenAi

prompt_sistema_resposta_api = f'''
    # Contexto

- Você é um chatbot especializado na cultura do Grupo J&F, possuindo amplo conhecimento sobre seus valores, missões, crenças, entre outros. Seu linguajar é natural e apropriado.

# Missão

- Sua missão é compreender as solicitações do usuário e fornecer respostas que agreguem valor, esclareçam dúvidas ou respondam a afirmações de maneira construtiva.

# Instruções

- A FORMATAÇÃO DA RESPOSTA DEVE SER EM LISTA E SUB-LISTAS
- Compreenda detalhadamente a solicitação do usuário, associe-a à cultura do Grupo J&F. Seja claro na resposta e evite usar muitos tokens. Aborde esta tarefa metodicamente, sem pressa e sem pular etapas.
- RESPONDA SOMENTE SE ESTIVER RELACIONADO A ISSO. Qualquer outra solicitação será respondida com esta mensagem que explica o porquê de não poder esclarecer.MENSAGEM: "Por favor insira mais detalhes de sua solicitação por conta que"[COMPLEMENTE COM O PORQUE DO NÃO PODER RESPONDER].
- Além de tudo isso, para tornar a mensagem mais interativa, insira emojis relacionados com a sua resposta.

# Exemplo

- Usuário: "meu colega me excluiu de um trabalho em grupo, no que ele deve melhorar e o que devo falar para ele?"
- ChatBot: "🔍 Para Melhorar: Seu colega pode focar em:

TRABALHO EM EQUIPE 🤝: Reconhecer a importância de incluir todos e trabalhar juntos, respeitando a contribuição de cada um.
COMPROMISSO COM O GRUPO 🌟: Entender que o sucesso do grupo depende da participação e colaboração de todos.
🗣️ O que Dizer:

EXPRESSE SEUS SENTIMENTOS 💬: Diga como se sentiu excluído e a importância de trabalhar juntos.
VALORES DO INSTITUTO GERMINARE 🏫: Lembre-o de que a atitude de dono inclui comprometimento com o grupo e colaboração.
CRESCIMENTO CONJUNTO 📈: Enfatize que todos no grupo têm algo valioso a contribuir para o sucesso coletivo.
Espero que isso ajude a melhorar a dinâmica do grupo! 🌟"

#Base De Dados
"""
'''

# Segunda parte, HISTORICO

#Variavieis globais   
cont_requisicao = 0
lista_historico = ["","",""]

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
        global cont_requisicao
        global prompt_sistema_resposta_api
        global lista_historico
        if(cont_requisicao == 0):
        
            pergunta_usuario = request.form['inputMessage']

            print(pergunta_usuario)
            #Api GPT
            pergunta_usuario = pergunta_usuario+" Além de tudo isso, para tornar a mensagem mais interativa, insira emojis relacionados com a sua resposta."
            resposta_identifica_arquivo = funcoes_OpenAi.identifica_arquivo(pergunta_usuario)

            dados_arquivo = funcoes_OpenAi.carrega(resposta_identifica_arquivo)

            resposta = funcoes_OpenAi.respostaApi(pergunta_usuario,dados_arquivo,prompt_sistema_resposta_api)
            cont_requisicao=cont_requisicao+1
            lista_historico[cont_requisicao] = f"""#CONVERSA ANTERIOR {cont_requisicao}
    -Solicitação anterior do usuário:
    {pergunta_usuario}
    -Resposta anterior:
    {resposta}
    """
            prompt_sistema_resposta_api = f'''
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
            resposta = resposta.replace("*","")
            return jsonify({'resposta': resposta})
        elif(cont_requisicao == 1):
            print("1")

            pergunta_usuario = request.form['inputMessage']

            print(pergunta_usuario)
            #Api GPT
            pergunta_usuario = pergunta_usuario+" Além de tudo isso, para tornar a mensagem mais interativa, insira emojis relacionados com a sua resposta."
            resposta_identifica_arquivo = funcoes_OpenAi.identifica_arquivo(pergunta_usuario)

            dados_arquivo = funcoes_OpenAi.carrega(resposta_identifica_arquivo)

            # prompt_sistema_respostaApi += listaHistorico[variavelGlobal] + listaHistorico[variavelGlobal+1]
            
            resposta = funcoes_OpenAi.respostaApi(pergunta_usuario,dados_arquivo,prompt_sistema_resposta_api+lista_historico[cont_requisicao] + lista_historico[cont_requisicao+1])
            cont_requisicao = cont_requisicao+1
            lista_historico[cont_requisicao] = f'''#CONVERSA ANTERIOR {cont_requisicao}
    -Solicitação anterior do usuário:
    {pergunta_usuario}
    -SUA RESPOSTA PARA A SOLICITAÇÃO:
    {resposta}
    """
    '''
            #Api GPT
            # Passa a variável para o template HTML
            # return render_template('index.html', variavel_frontend=resposta)
            resposta = resposta.replace("*","")
            return jsonify({'resposta': resposta})

        else:
            print("2")

            pergunta_usuario = request.form['inputMessage']

            print(pergunta_usuario)
            #Api GPT
            pergunta_usuario = pergunta_usuario
            resposta_identifica_arquivo = funcoes_OpenAi.identifica_arquivo(pergunta_usuario)
            
            dados_arquivo = funcoes_OpenAi.carrega(resposta_identifica_arquivo)
            
            resposta = funcoes_OpenAi.respostaApi(pergunta_usuario,dados_arquivo,prompt_sistema_resposta_api+lista_historico[cont_requisicao] + lista_historico[cont_requisicao-1])
            cont_requisicao = cont_requisicao-1
            lista_historico[cont_requisicao] = f'''#CONVERSA ANTERIOR {cont_requisicao}
    -Solicitação anterior do usuário:
    {pergunta_usuario}
    -Resposta anterior:
    {resposta}
    """
    '''
            #Api GPT
            # Passa a variável para o template HTML
            # return render_template('index.html', variavel_frontend=resposta)
            resposta = resposta.replace("*","")
            return jsonify({'resposta': resposta})

    except:
        
        return jsonify({'resposta': 'Algo ocoorreu de errado, tente novamente'})

app.run(debug=True)
