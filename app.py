from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
import re

app = Flask(__name__)
usuarios = {}

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    from_number = request.values.get("From", "")
    incoming_msg = request.values.get("Body", "").strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

    # Inicializa usuário
    if from_number not in usuarios:
        usuarios[from_number] = {}

    user = usuarios[from_number]

    # Saudações e disparo do menu
    if any(tag in incoming_msg for tag in ["oi", "olá", "bom dia", "boa tarde", "boa noite", "início", "menu", "começar", "homeflix", "e aí", "fala bot"]):
        user["estado"] = "menu"
        msg.body("🎉 *Seja bem-vindo(a) ao HOMEFLIX!*\nEu sou o HomeBot, seu guia oficial nessa maratona cheia de séries, filmes e memes. 😄🍿\n\nEscolha o que você quer:\n\n"
                 "⿡ *1️⃣ Falar com um atendente humano* (sim, de carne e osso 😎)\n"
                 "⿢ *2️⃣ Testar por 3 horinhas grátis* 🎁\n"
                 "⿣ *3️⃣ Ver os planos que até o Sheldon aprovaria* 💳\n\n👉 Digita *1*, *2* ou *3* e já começamos!")

    # Falar com atendente
    elif incoming_msg in ["1", "falar com atendente", "quero ajuda", "atendimento", "quero suporte", "atendente"]:
        msg.body("📡 Chamando reforços humanos!\nNosso atendente vai aparecer mais rápido que o Flash com uma xícara de café ☕💨. Aguarde um pouquinho! 😎")

    # Solicitar teste
    elif incoming_msg in ["2", "teste", "quero o teste", "teste grátis", "testar", "3 horas"]:
        user["estado"] = "aguardando_teste"
        msg.body("🎁 *Bora testar o HOMEFLIX por 3 horinhas!*\nSó preciso de duas coisinhas:\n\n👉 *Seu nome completo*\n👉 *Dispositivo* (ex: Smart TV LG, Fire Stick, TV Box...)")

    elif user.get("estado") == "aguardando_teste":
        user["dados_teste"] = incoming_msg
        msg.body("✅ Prontinho, seus dados foram recebidos!\nHomeBot já tá preparando o acesso. E você? Já pegou a pipoca? 🍿")

    # Visualizar planos
    elif incoming_msg in ["3", "planos", "quero ver os planos", "ver planos", "valores", "quais são os planos"]:
        msg.body("💳 *Planos HOMEFLIX™* — do casual ao maratonista full HD:\n\n"
                 "📆 *1 Mês – R$29,90*\nPerfeito pra quem quer experimentar sem compromisso (spoiler: você vai se apaixonar 😅).\n\n"
                 "📆 *6 Meses – R$149,90*\nSai por R$24,98/mês! Ótimo pra quem não perde um episódio. 🧠💰\n\n"
                 "📆 *12 Meses – R$239,90*\nSai por R$19,99/mês! Mais em conta que combo de pipoca no cinema. 🎬🤑\n\n"
                 "✨ E claro: todos os planos incluem acesso em qualidade *HD, Full HD e 4K Ultra*!\nSem taxa extra, sem limites, só diversão.\n\nDigite *menu* se quiser voltar pro início, ou mande sua escolha!")

    # Qualquer outra coisa
    else:
        msg.body("🤔 O HomeBot ainda tá tentando decifrar sua mensagem...\nMas não tem problema! Digita *menu* pra ver as opções ou escreve de outro jeitinho que eu entendo. 😅")

    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
