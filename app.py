from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
import random

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").lower().strip()
    resp = MessagingResponse()
    msg = resp.message()

    # Saudações variadas com emojis
    greetings = [
        "👋 Olá! Seja bem-vindo!",
        "😊 Oi! Pronto pra conversar?",
        "🙌 E aí! Como posso te ajudar hoje?"
    ]

    # Fluxo de atendimento
    if incoming_msg in ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite"]:
        msg.body(random.choice(greetings) + 
            "\n\n📋 *Menu principal:*\n1️⃣ Informações sobre o bot\n2️⃣ Horário de atendimento\n3️⃣ Falar com humano\n4️⃣ Ajuda geral")
    
    elif incoming_msg == "1":
        msg.body("🤖 Sou um bot inteligente que responde mensagens automaticamente pelo WhatsApp. Estou aqui pra facilitar sua vida!")
    
    elif incoming_msg == "2":
        msg.body("⏰ Nosso horário de atendimento é:\n🗓️ Segunda a sexta\n🕘 Das 9h às 18h\n📞 Fale com a gente sempre que precisar!")
    
    elif incoming_msg == "3":
        msg.body("🧍 Aguarde um momento...\n🔔 Um atendente humano será notificado e responderá em breve.")
    
    elif incoming_msg == "4":
        msg.body("📖 *Central de ajuda:*\nDigite uma palavra-chave como:\n🔹 'preço'\n🔹 'entrega'\n🔹 'pagamento'\n🔹 'cancelamento'\nOu envie *menu* para retornar às opções.")
    
    elif "preço" in incoming_msg:
        msg.body("💸 Os preços variam de acordo com o serviço escolhido.\n📦 Me diga o nome do produto que deseja consultar!")
    
    elif "entrega" in incoming_msg:
        msg.body("🚚 Nossas entregas são realizadas em até *3 dias úteis* na região metropolitana.\n✈️ Para outras regiões, consulte um atendente.")
    
    elif "pagamento" in incoming_msg:
        msg.body("💳 Aceitamos: Pix 🟢 | Cartão de crédito 💳 | Débito 💰 | Boleto 📄")
    
    elif "cancelamento" in incoming_msg:
        msg.body("⚠️ Para cancelar um pedido, envie o número do pedido ou digite *3* para falar com um atendente.")
    
    elif "menu" in incoming_msg:
        msg.body("📋 *Menu principal:*\n1️⃣ Informações sobre o bot\n2️⃣ Horário de atendimento\n3️⃣ Falar com humano\n4️⃣ Ajuda geral")
    
    else:
        msg.body("❓ Não entendi sua mensagem...\nVocê pode digitar *menu* para ver as opções ou enviar uma pergunta mais clara. Estou aqui pra ajudar! 😊")

    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
