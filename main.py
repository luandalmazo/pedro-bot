import os
import telebot
from bs4 import BeautifulSoup
import requests
from threading import Thread
import schedule
from time import sleep

''' Configs '''
TOKEN = ""
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
  "*/ensalamento* - Envia o link do ensalamento do curso"]

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
    print(message.chat.id)
    
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

def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)

def anuncio():
    return "something"

''' Infinite loop to keep the bot running '''
Thread(target=bot.polling).start()
schedule.every().monday.at("10:00").do(anuncio)
Thread(target=schedule_checker).start()