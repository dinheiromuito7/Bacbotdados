import logging
import pandas as pd
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Configuração do logging (para ver erros e logs no console)
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Token do bot (substitua spelo seu token do BotFather)
TOKEN = 7643009751:AAEhqknTm89Z3pVnLT7UchgKKIma7bp9-S4

# Histórico dos últimos resultados (simulação)
historico_resultados = [
    (6, 4), (5, 6), (7, 7), (4, 3), (8, 6), (2, 5), (6, 6), (3, 7), (5, 4), (6, 2)
]

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("🤖 Olá! Sou um bot de análise do Bac Bo. Envie /palpite para receber uma sugestão de aposta!")

def sugerir_aposta(update: Update, context: CallbackContext) -> None:
    if len(historico_resultados) < 5:
        update.message.reply_text("Aguarde mais resultados para análise.")
        return

    df = pd.DataFrame(historico_resultados, columns=['Azul', 'Vermelho'])

    # Contar ocorrências de cada resultado
    azul_vitorias = sum(df['Azul'] > df['Vermelho'])
    vermelho_vitorias = sum(df['Vermelho'] > df['Azul'])
    empates = sum(df['Azul'] == df['Vermelho'])

    total_jogos = len(df)

    # Calcular probabilidades
    prob_azul = azul_vitorias / total_jogos
    prob_vermelho = vermelho_vitorias / total_jogos
    prob_empate = empates / total_jogos

    # Determinar a aposta com maior probabilidade
    max_prob = max(prob_azul, prob_vermelho, prob_empate)

    if max_prob == prob_azul:
        aposta = "Azul"
    elif max_prob == prob_vermelho:
        aposta = "Vermelho"
    else:
        aposta = "Empate"

    # Calcular nível de confiança
    segunda_maior_prob = sorted([prob_azul, prob_vermelho, prob_empate])[-2]
    diferenca = max_prob - segunda_maior_prob

    if diferenca > 0.20:
        nivel_confiança = "🔵🔴 **ALTA**"
    elif diferenca > 0.10:
        nivel_confiança = "🟡 **MÉDIA**"
    else:
        nivel_confiança = "⚪ **BAIXA**"

    mensagem = (
        f"📊 **Análise dos últimos {total_jogos} jogos:**\n"
        f"🔵 Azul: {azul_vitorias} vitórias ({prob_azul:.1%})\n"
        f"🔴 Vermelho: {vermelho_vitorias} vitórias ({prob_vermelho:.1%})\n"
        f"⚪ Empates: {empates} ({prob_empate:.1%})\n\n"
        f"🎯 **Sugestão de aposta:** {aposta}\n"
        f"📈 **Nível de confiança:** {nivel_confiança}"
    )

    update.message.reply_text(mensagem, parse_mode="Markdown")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("palpite", sugerir_aposta))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
