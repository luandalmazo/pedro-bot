import os
import telebot
from bs4 import BeautifulSoup
import requests
import urllib.request
import json

''' Configs '''
TOKEN = "YOUR_TOKEN"
bot = telebot.TeleBot(TOKEN)

comandos = ["*/apresentar* - Apresenta o bot",
 "*/grade* - Envia a grade horária do curso",
  "*/processo* - Mostra os processos seletivos para o curso de IBM",
  "*/novoprocesso* - Cria um novo processo seletivo: Envie /novoprocesso + descrição do processo seletivo",
  "*/info* - Mostra informações sobre o curso",
  "*/help* - Mostra os comandos disponíveis",
  "*/datas* - Mostra as datas importantes do curso: Envie /datas + um mês por extenso",
  "*/ru* - Mostra o cardápio do RU",
  "*/eventos* - Mostra os eventos do curso",
  "*/novoevento - Cria um novo evento: Envie /novoevento + descrição do evento",
  "*/acervo* - Envia o link do acervo de conteúdos do curso",
  "*/sugestoes* - Envia sugestões de funcionalidades para o bot | Envie /sugestão + sua sugestão",
  "*/discord* - Envia o link do discord do curso",
  "*/ensalamento* - Envia o link do ensalamento do curso",
  "*/pesquisarsala* - Procura pelo ensalamento de uma discíplina | Envie /pesquisar_sala + nome da disciplina (ou código)",
  "*/man* - Instruções sobre comandos"]

''' Commands'''
@bot.message_handler(commands=['apresentar'])
def welcome(message):
    bot.reply_to(message, "Olá, eu sou o Pedro")

@bot.message_handler(commands=['help'])
def help(message):
    r = ""
    for c in comandos:
        r += c + "\n"

    bot.reply_to(message, r)

''' Function that send a message that is a pdf of the academic grade'''
@bot.message_handler(commands=['grade'])
def grade(message):
    bot.reply_to(message, "Aqui está a grade horária do curso")
    pdf = open('grade.pdf', 'rb')
    bot.send_document(message.chat.id, pdf)

@bot.message_handler(commands=['processo'])
def processo(message):

    ''' If the file is empty, it will send a message saying that there is no process'''
    if os.stat("processos.txt").st_size == 0:
        bot.reply_to(message, "Não há processos seletivos cadastrados no momento")
    else:
        ''' Read the file with the processos seletivos'''
        r = "*Aqui estão os processos seletivos abertos no momento:*\n"
        with open("processos_seletivos.txt", "r") as f:
            for line in f:
                r += line + "\n"
    
    bot.reply_to(message, r)

@bot.message_handler(commands=['novoprocesso'])
def novoprocesso(message):
    comando = message.text
    comando = comando.replace("/novoprocesso", "")
    comando = comando.replace("@PedroRealBot", "")

    if comando == "":
        bot.reply_to(message, "Envie o comando /novoprocesso + descrição do processo seletivo")
    else:
        file = open('processos_seletivos.txt', 'a')
        file.write(message.text[13:] + '\n')
        file.close()
        bot.reply_to(message, "Processo seletivo adicionado com sucesso")
    

@bot.message_handler(commands=['info'])
def info(message):
    bot.reply_to(message, "Neste link estão algumas informações sobre o curso")
    bot.reply_to(message, "https://web.inf.ufpr.br/infobiomedica/")

@bot.message_handler(commands=['datas'])
def datas(message):
    comando = message.text
    comando = comando.replace("/datas", "")
    if (comando == ""):
        bot.reply_to(message, "Envie o comando /datas + mês [por exemplo: /datas outubro]")
    elif (comando.find("outubro") != -1):
        bot.send_photo(message.chat.id, photo = open('datas/outubro-1.png', 'rb'))
        bot.send_photo(message.chat.id, photo = open('datas/outubro-2.png', 'rb'))
    elif (comando.find("novembro") != -1):
        bot.send_photo(message.chat.id, photo = open('datas/novembro.png', 'rb'))
    elif (comando.find("dezembro") != -1):
        bot.send_photo(message.chat.id, photo = open('datas/dezembro.png', 'rb'))
    elif (comando.find("janeiro") != -1):
        bot.send_photo(message.chat.id, photo = open('datas/janeiro.png', 'rb'))
    elif (comando.find("fevereiro") != -1):
        bot.send_photo(message.chat.id, photo = open('datas/fevereiro.png', 'rb'))
    elif (comando.find("março") != -1):
        bot.send_photo(message.chat.id, photo = open('datas/marco.png', 'rb'))
    else:
        bot.reply_to(message, "Mês inválido")
        
@bot.message_handler(commands=['ru'])
def ru(message):
    URL = "https://pra.ufpr.br/ru/ru-centro-politecnico/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all('figure', attrs={'class':'wp-block-table'})
   
    all_p = soup.select('p > strong')
    days = []
    for p in all_p:
        if (p.text.find('Seg') != -1) or p.text.find('Ter') != -1 or p.text.find('Qua') != -1 or p.text.find('Qui') != -1 or p.text.find('Sex') != -1:
            days.append(p.text)

    answer = ""
    i = 0
    ''' Show table data in a message of telegram bot'''
    for t in table:
        answer += days[i] + '\n'
        ''' Get the table and parse it to a string''' 
        for row in t.findAll('tr'):
            for cell in row.findAll('td'):
                if cell.text.startswith("CAFÉ"):
                    answer += f"*{cell.text}*" + " "
                elif cell.text.startswith("ALMOÇO"):
                    answer += f"*{cell.text}*" + " "
                elif cell.text.startswith("JANTAR"):
                    answer += f"*{cell.text}*" + " "
                else:
                    answer += cell.text + " "
                answer += "\n"
        answer += "\n"
        i += 1

    bot.reply_to(message, answer, parse_mode="Markdown")
    
@bot.message_handler(commands=['eventos'])
def eventos(message):
    
    ''' If the file is empty, send a message'''
    if os.stat("eventos.txt").st_size == 0:
        bot.reply_to(message, "Não há eventos cadastrados")
    else:
        r = "*Aqui estão os eventos para o curso*" + "\n"
        ''' Read the file with the eventos'''
        with open("eventos.txt", "r") as f:
            for line in f:
                r += line + "\n"
        
        bot.reply_to(message, r)


@bot.message_handler(commands=['novoevento'])
def novoevento(message):
    comando = message.text
    comando = comando.replace("/novoevento", "")
    comando = comando.replace("@PedroRealBot", "")

    if comando == "":
        bot.reply_to(message, "Envie o comando /novoevento + descrição do evento")
    else:
        file = open('eventos.txt', 'a')
        file.write(message.text[12:] + '\n')
        file.close()
        bot.reply_to(message, "Evento adicionado com sucesso")

@bot.message_handler(commands=['acervo'])
def drive(message):
    bot.reply_to(message, "Aqui está o link do acervo do curso")
    bot.reply_to(message, "https://linktr.ee/acervo_ibm")

@bot.message_handler(commands=['sugestoes'])
def sugestoes(message):
    ''' Catch the message and store it in a file'''
    comando = message.text
    comando = comando.replace("/sugestoes", "")
    comando = comando.replace("@PedroRealBot", "")
    if comando == "":
        bot.reply_to(message, "Envie o comando /sugestoes + sua sugestão")
    else:
        file = open('sugestoes.txt', 'a')
        file.write(message.text[10:] + '\n')
        file.close()
        bot.reply_to(message, "Sugestão enviada com sucesso")

@bot.message_handler(commands=['discord'])
def discord(message):
    bot.reply_to(message, "Aqui está o link do discord do curso")
    bot.reply_to(message, "https://discord.gg/kE4rcGtvMp")
  
@bot.message_handler(commands=['ensalamento'])
def ensalamento(message):
    bot.reply_to(message, "Aqui está o link para o ensalamento")
    bot.reply_to(message, "https://ensalamento.c3sl.ufpr.br/")

@bot.message_handler(commands=['pesquisarsala'])
def pesquisar_sala(message):
    comando = message.text
    comando = comando.replace("/pesquisarsala", "")
    comando = comando.replace("@PedroRealBot", "")
    comando = comando.replace(" ", "")
    if comando == "":
        bot.reply_to(message, "Envie o comando /pesquisarsala + nome da discíplina\nPrefira pesquisar pelo código da disciplina!")
    else:
        API = f"https://ensalamento.c3sl.ufpr.br/api/disciplinas/search?query={comando}"        
        r = ""
        try:
            url = urllib.request.urlopen(API)
            data = url.read()
            json_data = json.loads(data)
        except: 
            bot.reply_to(message, "Ocorreu um erro!") 

        try:
            for data in json_data["turmas"]:
                r += "*"+data["nome"]+"*" + "\n"
                for d in data["turmas"]:
                    for p in d["professores"]:
                        r += "Professores: "+p["nome"] + ","
                    r+="\n"
                    try:
                        for h in d["horarios"]:
                            r += "Horarios: "+str(h["dia"]) + "ª " + str(h["horario_inicial"]) + " - " + str(h["horario_final"]) + "\n"
                            r += "Sala: "+h["salaCode"] + "\n"
                            r += "\n"
                    except:
                        r += "Horarios: Não informado" + "\n"
                        r += "Sala: Não informado" + "\n"
                        r += "\n"
            bot.reply_to(message, r, parse_mode="Markdown")
        except:
            bot.reply_to(message, "Disciplina não encontrada")  
    
@bot.message_handler(commands=['man'])
def man(message):
    comando = message.text
    comando = comando.replace("/man", "")
    comando = comando.replace("@PedroRealBot", "")
    
    r = ""
    if comando == "":
        r = "Envie o comando /man + nome do comando\n*Opções disponíveis:\n*"
        r += "/man apresentar\n"
        r += "/man grade\n"
        r += "/man processo\n"
        r += "/man novo processo\n"
        r += "/man info\n"
        r += "/man help\n"
        r += "/man datas\n"
        r += "/man ru\n"
        r += "/man eventos\n"
        r += "/man novoevento\n"
        r += "/man acervo\n"
        r += "/man sugestoes\n"
        r += "/man discord\n"
        r += "/man ensalamento\n"
        r += "/man pesquisarsala\n"

    elif comando.find("apresentar") != -1:
        r = "Este comando apresenta o Pedro, e enviará o link do repositório que ele se encontra!"
    elif comando.find("grade") != -1:
        r = "Este comando enviará a grade do curso de Informática Biomédica por PDF!\n*Observação: este comando as vezes pode demorar alguns milisegundos para responder!*"
    elif comando.find("processo") != -1:
        r = "Este comando enviará a descrição de todos os processos seletivos abertos até o momento!"
    elif comando.find("novoprocesso") != -1:
        r = "Neste comando você pode acrescentar um novo processo seletivo.\nEnvie: /novoprocesso + descrição do processo seletivo\n"
        r += "*Exemplo: /novoprocesso Processo seletivo para bolsista de extensão | Link: -- | Data: --*"
    elif comando.find("info") != -1:
        r = "Este comando enviará o link para o site do curso de Informática Biomédica que contém informações sobre o curso como um todo!"
    elif comando.find("help") != -1:
        r = "Este comando enviará uma lista de comandos que eu posso realizar!"
    elif comando.find("datas") != -1:
        r = "Este comando enviará fotos contendo as datas para o respectivo mês!\n"
        r += "*Exemplo: /datas outubro*"
        r += "\nObservação: envie o nome do mês por extenso!"
    elif comando.find("ru") != -1:
        r = "Este comando enviará o cardápio do RU para os próximos dias!\n"
        r += "*Observação: este comando as vezes pode demorar alguns milisegundos para responder!*"
    elif comando.find("eventos") != -1:
        r = "Este comando enviará uma lista de eventos que estão acontecendo no curso!"
    elif comando.find("novoevento") != -1:
        r = "Neste comando você pode acrescentar um novo evento\nEnvie: /novoevento + descrição do evento\n"
        r += "*Exemplo: /novoevento SABER | Link: -- | Data: --*"
    elif comando.find("acervo") != -1:
        r = "Este comando enviará o link para o acervo do curso de Informática Biomédica!"
    elif comando.find("sugestoes") != -1:
        r = "Neste comando você pode mandar uma sugestão para o Pedro!\nEnvie: /sugestoes + sua sugestão\n"
        r += "*Exemplo: /sugestoes O Pedro deveria ter outro nome!*"
    elif comando.find("discord") != -1:
        r = "Este comando enviará o link para o servidor do Discord do curso de Informática Biomédica!"
    elif comando.find("ensalamento") != -1:
        r = "Este comando enviará o link para o site do ensalamento do C3SL!"
    elif comando.find("pesquisarsala") != -1:
        r = "Neste comando você pode pesquisar a sua sala!\nEnvie: /pesquisarsala + nome da disciplina"
        r += "\n*Exemplo: /pesquisarsala ci1055\n*"
        r += "\nObservação: Prefira pesquisar pelo código da disciplina, pelo nome posso ter dificuldades em achar!"
    else:
        r  = "Comando não encontrado"
    bot.reply_to(message, r, parse_mode="Markdown")


''' Infinite loop to keep the bot running '''
bot.polling()