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

    # Inicializa estado do usuário
    if from_number not in usuarios:
        usuarios[from_number] = {"estado": "menu", "humano": False}

    user = usuarios[from_number]

    # 🎛️ Controle do modo humano
    if "modo humano on" in incoming_msg:
        user["humano"] = True
        msg.body("🤐 HomeBot entrou no modo silêncio!\nAgora o atendimento é 100% humano. Chama o cafezinho! ☕")
        return str(resp)

    if "modo humano off" in incoming_msg:
        user["humano"] = False
        msg.body("🗣️ HomeBot de volta ao palco!\nPode mandar que eu tô online pra responder. 🎬🍿")
        return str(resp)

    # 🚫 Se modo humano estiver ativado, não responde
    if user.get("humano") is True:
        return str(resp)

    # 👋 Saudações e exibir menu
    if any(tag in incoming_msg for tag in ["oi", "olá", "menu", "início", "homeflix", "fala bot", "começar", "bom dia", "boa tarde", "boa noite"]):
        user["estado"] = "menu"
        msg.body("🎉 *E aí! Eu sou o HomeBot da HOMEFLIX!*\n\nPronto pra começar sua jornada maratonística?\nEscolha uma das opções abaixo e me diga o número:\n\n"
                 "⿡ *1️⃣ Falar com um atendente humano* (sim, de carne e osso 😎)\n"
                 "⿢ *2️⃣ Testar por 3 horinhas grátis* 🎁\n"
                 "⿣ *3️⃣ Ver os planos que até o Sheldon aprovaria* 💳\n\n👉 Digita *1*, *2* ou *3* pra continuar.")

    # 🧍 Falar com atendente
    elif incoming_msg in ["1", "atendimento", "atendente", "quero ajuda", "falar com atendente", "suporte"]:
        msg.body("📡 HomeBot acionando reforços humanos!\nNosso atendente real vai aparecer mais rápido que uma abertura de série. 🎬😄")

    # 🎁 Solicitar teste
    elif incoming_msg in ["2", "teste", "quero testar", "teste grátis", "3 horas", "testar"]:
        user["estado"] = "aguardando_teste"
        msg.body("🎁 *Teste gratuito de 3 horas ativado!*\n\nManda pra mim:\n👉 *Seu nome completo*\n👉 *Dispositivo* (ex: Smart TV LG, Fire Stick, TV Box...)")

    # Receber dados do teste
    elif user.get("estado") == "aguardando_teste":
        user["dados_teste"] = incoming_msg
        user["estado"] = "menu"
        msg.body("✅ Show! Recebi os dados direitinho.\nVou liberar seu acesso de teste rapidinho. Enquanto isso... já escolheu o que vai maratonar? 🍿📺")

    # 💳 Ver planos
    elif incoming_msg in ["3", "ver planos", "quero plano", "quais são os planos", "planos", "valores"]:
        msg.body("💳 *Planos HOMEFLIX™* — só alegria:\n\n"
                 "📅 *1 Mês – R$29,90*\nIdeal pra testar as águas… ou mergulhar de cabeça! 🏖️\n\n"
                 "📅 *6 Meses – R$149,90*\nSai a R$24,98/mês — mais econômico, sem perder a maratona! 🎯\n\n"
                 "📅 *12 Meses – R$239,90*\nSai a R$19,99/mês — plano dos maratonistas sérios. 😎📆\n\n"
                 "✨ Todos incluem acesso em *HD, FHD e até 4K Ultra*!\nNada de taxas extras, só conteúdo de primeira. 🎥🍿\n\nDigite *menu* pra voltar ou já manda o plano desejado!")

    # 🛑 Mensagem não reconhecida
    else:
        msg.body("🤖 O HomeBot ainda tá tentando entender essa mensagem...\nMas não se preocupe! Digita *menu* pra ver as opções ou manda sua dúvida que eu desenrolo pra você. 😄")

    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
