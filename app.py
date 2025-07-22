from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
import re

app = Flask(__name__)
usuarios = {}

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    from_number = request.values.get("From", "")
    incoming_msg = request.values.get("Body", "").strip()
    resp = MessagingResponse()
    msg = resp.message()

    # Inicia perfil do usuário
    if from_number not in usuarios:
        usuarios[from_number] = {}
    
    user = usuarios[from_number]
    texto = incoming_msg.lower()

    # 🔍 Captura nome
    nome_match = re.search(r"(meu nome é|nome:)\s*([a-zà-ÿ\'\s]+)", texto, re.IGNORECASE)
    if nome_match:
        user["nome"] = nome_match.group(2).strip().title()

    # 📧 Captura email
    email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", texto)
    if email_match:
        user["email"] = email_match.group(0)

    # 📦 Captura plano ou teste
    if "1 mês" in texto:
        user["plano"] = "📆 Plano de 1 mês – R$29,90"
    elif "6 meses" in texto:
        user["plano"] = "📆 Plano de 6 meses – R$149,90"
    elif "12 meses" in texto:
        user["plano"] = "📆 Plano de 12 meses – R$239,90"
    elif "teste" in texto:
        user["plano"] = "🎁 Teste gratuito de 3 horas"

    # 🎯 Verifica se já tem tudo
    if "nome" in user and "email" in user and "plano" in user:
        resumo = "📋 *Resumo HOMEFLIX:*\n"
        resumo += f"👤 Nome: {user['nome']}\n"
        resumo += f"📧 Email: {user['email']}\n"
        resumo += f"🎁 Escolha: {user['plano']}\n\n"
        resumo += "✅ Tudo certo! Um atendente humano vai te responder em breve. Enquanto isso, que tal escolher uma pipoca pra essa maratona? 🍿😉"
        msg.body(resumo)
    else:
        msg.body("🎬 *E aí! Eu sou o HomeBot da HOMEFLIX e tô aqui pra agilizar sua inscrição!*\n\nMe manda tudo numa só mensagem, tipo assim:\n\n*Nome: Seu nome completo*\n*Email: seu@email.com*\n*Quero o plano de 6 meses ou o teste gratuito*\n\n✨ Assim eu registro tudo rapidinho e te respondo com o resumo. Vamo que vamo! 🚀")

    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
