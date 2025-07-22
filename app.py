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

    if from_number not in usuarios:
        usuarios[from_number] = {}

    user_data = usuarios[from_number]

    # 🧠 Identificar dados enviados juntos
    nome_match = re.search(r"(meu nome é|nome:)\s*([A-Za-zÀ-ÿ\'\s]+)", incoming_msg, re.IGNORECASE)
    email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", incoming_msg)
    telefone_match = re.search(r"\(?\d{2}\)?\s?\d{4,5}-?\d{4}", incoming_msg)
    
    if nome_match:
        user_data["nome"] = nome_match.group(2).strip().title()
    if email_match:
        user_data["email"] = email_match.group(0)
    if telefone_match:
        user_data["telefone"] = telefone_match.group(0)

    if "teste" in incoming_msg.lower():
        user_data["tipo"] = "Teste de 3 horas"
    elif "1 mês" in incoming_msg.lower():
        user_data["tipo"] = "Plano 1 mês – R$29,90"
    elif "6 meses" in incoming_msg.lower():
        user_data["tipo"] = "Plano 6 meses – R$149,90"
    elif "12 meses" in incoming_msg.lower():
        user_data["tipo"] = "Plano 12 meses – R$239,90"

    # 🎯 Menu principal
    if incoming_msg in ["oi", "olá", "ola", "menu", "homeflix", "início"]:
        msg.body("🎬 *Bem-vindo(a) à HOMEFLIX!*\n\nSelecione uma opção:\n"
                 "1️⃣ Falar com atendente\n"
                 "2️⃣ Solicitar teste grátis (3h)\n"
                 "3️⃣ Ver planos disponíveis\n"
                 "4️⃣ Qualidade de imagem\n"
                 "5️⃣ Enviar dados completos\n"
                 "6️⃣ Ver resumo")
    
    elif incoming_msg == "1":
        user_data["atendente"] = "Solicitado"
        msg.body("📞 Um atendente será notificado em breve.")
    
    elif incoming_msg == "2":
        user_data["tipo"] = "Teste de 3 horas"
        msg.body("✅ Teste de 3 horas registrado! Envie seu nome, e-mail e telefone para ativar.")
    
    elif incoming_msg == "3":
        msg.body("💳 *Planos disponíveis:*\n1 mês → R$29,90\n6 meses → R$149,90\n12 meses → R$239,90\nTodos incluem HD, FHD e 4K! 🔥")
    
    elif incoming_msg == "4":
        msg.body("📺 Qualidade de imagem:\n✅ HD\n✅ Full HD\n✅ 4K Ultra\nIncluídas em todos os planos!")

    elif incoming_msg == "5":
        msg.body("📨 Envie tudo numa única mensagem, como:\n*Nome: Fulano\nEmail: fulano@homeflix.com\nTelefone: (11) 91234-5678\nQuero o plano de 6 meses*")

    elif incoming_msg == "6" or "resumo" in incoming_msg.lower():
        if user_data:
            resumo = "📋 *Resumo HOMEFLIX:*\n"
            resumo += f"👤 Nome: {user_data.get('nome', 'não informado')}\n"
            resumo += f"📧 Email: {user_data.get('email', 'não informado')}\n"
            resumo += f"📞 Telefone: {user_data.get('telefone', 'não informado')}\n"
            resumo += f"🎁 Escolha: {user_data.get('tipo', 'não informado')}\n"
            msg.body(resumo + "\n✅ Um atendente entrará em contato em breve!")
        else:
            msg.body("🔍 Nenhum dado registrado. Envie as informações completas ou digite *menu* para começar.")

    else:
        msg.body("❓ Não entendi... Digite *menu* para ver as opções ou envie seus dados como:\n*Nome: Fulano, Email: fulano@...*, etc.")

    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
