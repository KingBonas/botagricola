import telebot
from telebot import types
import os
import pandas as pd
import matplotlib.pyplot as plt


TOKEN = '7021646927:AAFKwSOT9XSBrC8ig4XS9r73Fg8bI68_4Jk'

bot=telebot.TeleBot(TOKEN)

user_data={}

def limpar_dados_usuario(chat_id):
    if chat_id in user_data:
        del user_data[chat_id]

def resetar_bot():
    global user_data
    user_data = {}

def calculo_colheitabilidade_tempo(data):
    try:
        tch = float(data['tch'])
        coef_km = {
            "Alternado (4,167)": 4.167,
            "Simples (6,667)": 6.667,
            "Simples 2 Linhas (3,333)": 3.333
        }[data['coef_km']]
        velocidade_cd = float(data['velocidade']) - 0.8
        velocidade_fixa = float(data['velocidade'])
        tempo_produtivo = int(data['tempo_produtivo'])
        tempo_produtivo_v = int(data['tempo_produtivo']) - 20
        num_cd = int(data['num_cd'])

        resultado = []
        for i in range(10):
            velocidade_variada = velocidade_cd + 0.2 * i
            colheitabilidade = ((tch / coef_km) * velocidade_variada) * (tempo_produtivo / 60)
            produtividade_hora = colheitabilidade * num_cd

            resultado.append((f"{tempo_produtivo:.2f}", f"{velocidade_variada:.1f}", f"{colheitabilidade:.2f}", f"{produtividade_hora:.2f}"))
                    
        resultado2 = []
        for j in range(10):
            tempo_produtivo_v2 = tempo_produtivo_v + 5 * j
            colheitabilidade = ((tch / coef_km) * velocidade_fixa) * (tempo_produtivo_v2 / 60)
            
            resultado2.append((f"{tempo_produtivo_v2:.2f}", f"{colheitabilidade:.2f}"))
        
        return resultado, resultado2
        
    except (ValueError, KeyError):
        return None, None
    
def tabela_colheitabilidade_tempo1(results1):
    df = pd.DataFrame(results1, columns=['Tempo Produtivo (min)','Velocidade (km/h)', 'Colheitabilidade (ton/CD.h)', 'Produtividade Hora (ton.h)'])
    plt.figure(figsize=(10,6))
    plt.title("Colheitabilidade Tempo Fixo / Velocidade Variada:")
    table = plt.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

    for i in range(len(df.columns)):   
        cell = table[(5, i)]
        cell.set_facecolor('purple')
        cell.set_text_props(color='white', weight='bold')

    plt.axis('off')
    plt.savefig('result_table_tempo1.png', bbox_inches='tight')
    plt.close()

def tabela_colheitabilidade_tempo2(results2):
    df = pd.DataFrame(results2, columns=['Tempo Produtivo (min)', 'Colheitabilidade (ton/CD.h)'])
    plt.figure(figsize=(10,6))
    plt.title("Colheitabilidade Tempo Variado / Velocidade Fixa:")
    table = plt.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

    for i in range(len(df.columns)):   
        cell = table[(5, i)]
        cell.set_facecolor('purple')
        cell.set_text_props(color='white', weight='bold')
    
    plt.axis('off')
    plt.savefig('result_table_tempo2.png', bbox_inches='tight')
    plt.close()

def calculo_colheitabilidade_manobra(data):
    try:
        tch = float(data['tch'])
        coef_km = {
            "Alternado (4,167)": 4.167,
            "Simples (6,667)": 6.667,
            "Simples 2 Linhas (3,333)": 3.333
        }[data['coef_km']]
        velocidade_cd = float(data['velocidade']) - 0.8
        taxa_manobra = float(data['taxa_manobra']) / 100
        num_cd = int(data['num_cd'])

        resultado = []
        for i in range(10):
            velocidade_variada = velocidade_cd + 0.2 * i
            colheitabilidade = ((tch / coef_km) * velocidade_variada) * (1 - taxa_manobra)
            produtividade_hora = colheitabilidade * num_cd

            resultado.append((f"{velocidade_variada:.1f}", f"{colheitabilidade:.2f}", f"{produtividade_hora:.2f}"))       
    
        return resultado
        
    except (ValueError, KeyError):
        return None
    
def tabela_colheitabilidade_manobra(results1):
    df = pd.DataFrame(results1, columns=['Velocidade (km/h)', 'Colheitabilidade (ton/CD.h)', 'Produtividade Hora (ton.h)'])
    plt.figure(figsize=(10,6))
    plt.title("Calculo Colheitabilidade:")
    table = plt.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

    for i in range(len(df.columns)):   
        cell = table[(5, i)]
        cell.set_facecolor('purple')
        cell.set_text_props(color='white', weight='bold')
    
    plt.axis('off')
    plt.savefig('result_table_colheitabilidade.png', bbox_inches='tight')
    plt.close()

def calculo_dimensionamento_CD(data):
    try:
        tcd = float(data['tcd'])
        tch = float(data['tch'])
        velocidade_media_cd = float(data['velocidade']) - 0.8
        taxa_manobra = float(data['taxa_manobra']) / 100
        horas_produtivas = float(data['horas_produtivas'])
        espaçamento = {
            "Alternado (4,167)": 4.167,
            "Simples (6,667)": 6.667,
            "Simples 2 Linhas (3,333)": 3.333
        }[data['espaçamento']]

        resultado = []
        for i in range(10):
            velocidade_variada = velocidade_media_cd + 0.2 * i
            colheitabilidade = ((tch / espaçamento) * velocidade_variada) * (1 - taxa_manobra)
            produtividade_diaria = colheitabilidade * horas_produtivas
            n_cd = tcd / produtividade_diaria

            resultado.append((f"{velocidade_variada:.1f}", f"{colheitabilidade:.2f}", f"{produtividade_diaria:.2f}", f"{n_cd:.2f}"))

        return resultado

    except (ValueError, KeyError):
        return None
    
def tabela_dimensionamento_cd(results1):
    df = pd.DataFrame(results1, columns=['Velocidade (km/h)', 'Colheitabilidade (ton/CD.h)', 'Produtividade Diária (ton/dia)', 'Nº de Colhedoras'])
    plt.figure(figsize=(10,6))
    plt.title("Calculo Dimensionamento de Colhedora:")
    table = plt.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

    for i in range(len(df.columns)):   
        cell = table[(5, i)]
        cell.set_facecolor('purple')
        cell.set_text_props(color='white', weight='bold')
    
    plt.axis('off')
    plt.savefig('result_table_dimensionamentoCD.png', bbox_inches='tight')
    plt.close()

@bot.message_handler(commands=['start'])
def start(mensagem):
    resetar_bot()
    texto = """Bem-vindo à Calculadora Agrícola! Use os comandos para começar:\n
/colheitabilidade_tempo - Calcular Colheitabilidade por Tempo Produtivo\n
/colheitabilidade_manobra - Calcular Colheitabilidade por Taxa de Manobra\n
/dimensionamento_CD - Calcular Dimensionamento de Colhedora"""

    bot.send_message(mensagem.chat.id, texto)

@bot.message_handler(commands=['colheitabilidade_tempo'])
def colheitabilidade_tempo(message):
    limpar_dados_usuario(message.chat.id)
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id, "Digite o TCH [ton/ha]:")
    bot.register_next_step_handler(message, get_tch_tempo)

def get_tch_tempo(message):
    try:
        user_data[message.chat.id]['tch'] = float(message.text)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Alternado (4,167)', 'Simples (6,667)', 'Simples 2 Linhas (3,333)')
        bot.send_message(message.chat.id, "Escolha o Coef. Km Linear:", reply_markup=markup)
        bot.register_next_step_handler(message, get_coef_km_tempo)
    except ValueError:
        bot.send_message(message.chat.id, "Por favor, insira um número válido para o TCH.")
        bot.register_next_step_handler(message, get_tch_tempo)

def get_coef_km_tempo(message):
    user_data[message.chat.id]['coef_km'] = message.text
    bot.send_message(message.chat.id, "Digite a Velocidade Média CD [km/h]:")
    bot.register_next_step_handler(message, get_velocidade_tempo)

def get_velocidade_tempo(message):
    try:
        user_data[message.chat.id]['velocidade'] = float(message.text)
        bot.send_message(message.chat.id, "Digite o Nº de CD [un]:")
        bot.register_next_step_handler(message, get_num_cd_tempo)
    except ValueError:
        bot.send_message(message.chat.id, "Por favor, insira um número válido para a Velocidade Média.")
        bot.register_next_step_handler(message, get_velocidade_tempo)

def get_num_cd_tempo(message):
    try:
        user_data[message.chat.id]['num_cd'] = int(message.text)
        bot.send_message(message.chat.id, "Digite o Tempo Produtivo [min]:")
        bot.register_next_step_handler(message, get_tempo_produtivo)
    except ValueError:
        bot.send_message(message.chat.id, "Por favor, insira um número válido para o Nº de CD.")
        bot.register_next_step_handler(message, get_num_cd_tempo)

def get_tempo_produtivo(message):
    try:
        user_data[message.chat.id]['tempo_produtivo'] = int(message.text)
        results1, results2 = calculo_colheitabilidade_tempo(user_data[message.chat.id])
        if results1 and results2:
            tabela_colheitabilidade_tempo1(results1)
            tabela_colheitabilidade_tempo2(results2)
            bot.send_photo(message.chat.id, photo=open('result_table_tempo1.png', 'rb'))
            bot.send_photo(message.chat.id, photo=open('result_table_tempo2.png', 'rb'))
            os.remove('result_table_tempo1.png')
            os.remove('result_table_tempo2.png')
        else:
            bot.send_message(message.chat.id, "Erro ao calcular. Verifique os valores e tente novamente.")
    except ValueError:
        bot.send_message(message.chat.id, "Por favor, insira um número válido para o Tempo Produtivo.")
        bot.register_next_step_handler(message, get_tempo_produtivo)

@bot.message_handler(commands=['colheitabilidade_manobra'])
def colheitabilidade_manobra(message):
    limpar_dados_usuario(message.chat.id)
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id, "Digite o TCH [ton/ha]:")
    bot.register_next_step_handler(message, get_tch_manobra)

def get_tch_manobra(message):
    try:
        user_data[message.chat.id]['tch'] = float(message.text)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Alternado (4,167)', 'Simples (6,667)', 'Simples 2 Linhas (3,333)')
        bot.send_message(message.chat.id, "Escolha o Coef. Km Linear:", reply_markup=markup)
        bot.register_next_step_handler(message, get_coef_km_manobra)
    except ValueError:
        bot.send_message(message.chat.id, "Por favor, insira um número válido para o TCH.")
        bot.register_next_step_handler(message, get_tch_manobra)

def get_coef_km_manobra(message):
    user_data[message.chat.id]['coef_km'] = message.text
    bot.send_message(message.chat.id, "Digite a Velocidade Média CD [km/h]:")
    bot.register_next_step_handler(message, get_velocidade_manobra)

def get_velocidade_manobra(message):
    try:
        user_data[message.chat.id]['velocidade'] = float(message.text)
        bot.send_message(message.chat.id, "Digite o Nº de CD [un]:")
        bot.register_next_step_handler(message, get_num_cd_manobra)
    except ValueError:
        bot.send_message(message.chat.id, "Por favor, insira um número válido para a Velocidade Média.")
        bot.register_next_step_handler(message, get_velocidade_manobra)

def get_num_cd_manobra(message):
    try:
        user_data[message.chat.id]['num_cd'] = int(message.text)
        bot.send_message(message.chat.id, "Digite a Taxa de Manobra [%]:")
        bot.register_next_step_handler(message, get_taxa_manobra)
    except ValueError:
        bot.send_message(message.chat.id, "Por favor, insira um número válido para o Nº de CD.")
        bot.register_next_step_handler(message, get_num_cd_manobra)

def get_taxa_manobra(message):
    try:
        user_data[message.chat.id]['taxa_manobra'] = float(message.text)
        results1 = calculo_colheitabilidade_manobra(user_data[message.chat.id])
        if results1:
            tabela_colheitabilidade_manobra(results1)
            bot.send_photo(message.chat.id, photo=open('result_table_colheitabilidade.png', 'rb'))
            os.remove('result_table_colheitabilidade.png')
        else:
            bot.send_message(message.chat.id, "Erro ao calcular. Verifique os valores e tente novamente.")
    except ValueError:
        bot.send_message(message.chat.id, "Por favor, insira um número válido para a Taxa de Manobra.")
        bot.register_next_step_handler(message, get_taxa_manobra)

@bot.message_handler(commands=['dimensionamento_CD'])
def dimensionamento_CD(message):
    limpar_dados_usuario(message.chat.id)
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id, "Digite o TCD [ton]")
    bot.register_next_step_handler(message, get_tcd_dimensionamento)

def get_tcd_dimensionamento(message):
    try:
        user_data[message.chat.id]['tcd'] = float(message.text)
        bot.send_message(message.chat.id, "Digite o TCH [ton/ha]:")
        bot.register_next_step_handler(message, get_tch_dimensionamento)
    except ValueError:
        bot.send_message(message.chat.id, "Por favor, insira um número valido para o TCD.")
        bot.register_next_step_handler(message, get_tcd_dimensionamento)

def get_tch_dimensionamento(message):
    try:
        user_data[message.chat.id]['tch'] = float(message.text)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Alternado (4,167)', 'Simples (6,667)', 'Simples 2 Linhas (3,333)')
        bot.send_message(message.chat.id, "Escolha o Espaçamento:", reply_markup=markup)
        bot.register_next_step_handler(message, get_espaçamento_dimensionamento)
    except ValueError:
        bot.send_message(message.chat.id, "Por favor, insira um número válido para o TCH.")
        bot.register_next_step_handler(message, get_tch_dimensionamento)

def get_espaçamento_dimensionamento(message):
    user_data[message.chat.id]['espaçamento'] = message.text
    bot.send_message(message.chat.id, "Digite a Velocidade Média CD [km/h]:")
    bot.register_next_step_handler(message, get_velocidade_dimensionamento)

def get_velocidade_dimensionamento(message):
    try:
        user_data[message.chat.id]['velocidade'] = float(message.text)
        bot.send_message(message.chat.id, "Digite as Horas Produtivas [horas]:")
        bot.register_next_step_handler(message, get_horas_produtivas_dimensionamento)
    except ValueError:
        bot.send_message(message.chat.id, "Por favor, insira um número válido para a Velocidade Média.")
        bot.register_next_step_handler(message, get_velocidade_dimensionamento)

def get_horas_produtivas_dimensionamento(message):
    try:
        user_data[message.chat.id]['horas_produtivas'] = int(message.text)
        bot.send_message(message.chat.id, "Digite a Taxa de Manobra [%]:")
        bot.register_next_step_handler(message, get_taxa_manobra_dimensionamento)
    except ValueError:
        bot.send_message(message.chat.id, "Por favor, insira um número válido para o Nº de CD.")
        bot.register_next_step_handler(message, get_horas_produtivas_dimensionamento)

def get_taxa_manobra_dimensionamento(message):
    try:
        user_data[message.chat.id]['taxa_manobra'] = float(message.text)
        results1 = calculo_dimensionamento_CD(user_data[message.chat.id])
        if results1:
            tabela_dimensionamento_cd(results1)
            bot.send_photo(message.chat.id, photo=open('result_table_dimensionamentoCD.png', 'rb'))
            os.remove('result_table_dimensionamentoCD.png')
        else:
            bot.send_message(message.chat.id, "Erro ao calcular. Verifique os valores e tente novamente.")
    except ValueError:
        bot.send_message(message.chat.id, "Por favor, insira um número válido para a Taxa de Manobra.")
        bot.register_next_step_handler(message, get_taxa_manobra_dimensionamento)


bot.polling()