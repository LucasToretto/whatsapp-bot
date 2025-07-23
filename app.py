from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
import random

app = Flask(__name__)

# Armazenamento temporário dos usuários em memória (usado por número de telefone)
usuarios = {}

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    from_number = request.values.get("From", "")
    incoming_msg = request.values.get("Body", "").lower().strip()
    resp = MessagingResponse()
    msg = resp.message()

    # Inicializa dados do usuário se ainda não tiver
    if from_number not in usuarios:
        usuarios[from_number] = {}

    # Saudações e menu principal
    if incoming_msg in ["oi", "olá", "ola", "homeflix", "menu", "início"]:
        msg.body("🎬 Bem-vindo(a) à HOMEFLIX!\n\n📋 *Menu Principal:*\n"
                 "1️⃣ Falar com atendente\n"
                 "2️⃣ Solicitar teste grátis (3h)\n"
                 "3️⃣ Ver planos disponíveis\n"
                 "4️⃣ Qualidade de imagem\n"
                 "5️⃣ Enviar resumo das escolhas\n"
                 "6️⃣ Informar nome\n"
                 "7️⃣ Informar dispositivo")
    
    # Falar com atendente
    elif incoming_msg == "1":
        msg.body("📞 Um atendente humano será notificado. Aguarde um momento...")
        usuarios[from_number]["atendente"] = "Solicitado"

    # Solicitar teste
    elif incoming_msg == "2" or "teste" in incoming_msg:
        msg.body("✅ Teste de 3 horas ativável!\nEnvie seu nome e tipo de dispositivo para liberarmos o acesso.")
        usuarios[from_number]["teste"] = "Solicitado"

    # Ver planos
    elif incoming_msg == "3" or "planos" in incoming_msg:
        msg.body("💳 *Planos HOMEFLIX:*\n"
                 "1 mês → R$29,90\n"
                 "6 meses → R$149,90\n"
                 "12 meses → R$239,90\n\nTodos incluem HD, FHD e 4K! 🔥")
        usuarios[from_number]["planos"] = "Visualizado"

    # Qualidade de imagem
    elif incoming_msg == "4" or "qualidade" in incoming_msg:
        msg.body("📺 Imagens com qualidade:\n✅ HD\n✅ Full HD\n✅ 4K Ultra\nIncluídas em todos os planos!")

    # Informar nome
    elif incoming_msg.startswith("meu nome é"):
        nome = incoming_msg.replace("meu nome é", "").strip().title()
        usuarios[from_number]["nome"] = nome
        msg.body(f"📝 Nome registrado: *{nome}*")

    elif incoming_msg == "6":
        msg.body("📛 Envie seu nome usando o formato:\n*Meu nome é Joãozinho*")

    # Informar dispositivo
    elif incoming_msg.startswith("meu dispositivo é"):
        dispositivo = incoming_msg.replace("meu dispositivo é", "").strip().title()
        usuarios[from_number]["dispositivo"] = dispositivo
        msg.body(f"📱 Dispositivo registrado: *{dispositivo}*")

    elif incoming_msg == "7":
        msg.body("💻 Envie seu dispositivo usando o formato:\n*Meu dispositivo é TV / celular / notebook...*")

    # Resumo das escolhas
    elif incoming_msg == "5" or "resumo" in incoming_msg:
        dados = usuarios[from_number]
        if not dados:
            msg.body("🔍 Nenhuma informação foi registrada ainda.\nDigite *menu* para começar!")
        else:
            resumo = "📋 *Resumo do Cliente HOMEFLIX:*\n"
            for chave, valor in dados.items():
                resumo += f"🔹 {chave.capitalize()}: {valor}\n"
            msg.body(resumo)

    # Plano escolhido via texto livre
    elif "1 mês" in incoming_msg:
        usuarios[from_number]["plano"] = "1 mês - R$29,90"
        msg.body("🗓️ Plano registrado: *1 mês - R$29,90*")
    elif "6 meses" in incoming_msg:
        usuarios[from_number]["plano"] = "6 meses - R$149,90"
        msg.body("🗓️ Plano registrado: *6 meses - R$149,90*")
    elif "12 meses" in incoming_msg:
        usuarios[from_number]["plano"] = "12 meses - R$239,90"
        msg.body("🗓️ Plano registrado: *12 meses - R$239,90*")

    # Quando não entende
    else:
        msg.body("❓ Não entendi... Digite *menu* para ver as opções ou envie sua dúvida com mais detalhes!")

    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
