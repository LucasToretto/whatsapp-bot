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

    # Inicializa dados
    if from_number not in usuarios:
        usuarios[from_number] = {"estado": "menu"}

    user = usuarios[from_number]

    # Captura automática de dados
    nome_match = re.search(r"(meu nome é|nome:)\s*([a-zà-ÿ\'\s]+)", incoming_msg, re.IGNORECASE)
    email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", incoming_msg)
    telefone_match = re.search(r"\(?\d{2}\)?\s?\d{4,5}-?\d{4}", incoming_msg)

    if nome_match:
        user["nome"] = nome_match.group(2).strip().title()
    if email_match:
        user["email"] = email_match.group(0)
    if telefone_match:
        user["telefone"] = telefone_match.group(0)

    # Voltar pro menu principal
    if incoming_msg == "menu":
        user["estado"] = "menu"

    # Voltar pro submenu anterior
    elif incoming_msg == "voltar":
        user["estado"] = "menu"  # neste caso, sempre volta pro principal

    # Respostas baseadas no estado
    if user["estado"] == "menu":
        msg.body("🎬 *Bem-vindo(a) à HOMEFLIX!*\n\nVocê está no menu principal. Selecione uma opção:\n"
                 "1️⃣ Falar com um atendente humano\n"
                 "2️⃣ Solicitar teste grátis de 3h\n"
                 "3️⃣ Ver planos disponíveis\n"
                 "4️⃣ Saber sobre qualidade de imagem\n"
                 "5️⃣ Enviar dados completos (nome, email, telefone, plano)\n"
                 "6️⃣ Ver resumo das suas escolhas\n\nDigite o número da opção desejada:")

        user["estado"] = "menu_aguardando"

    elif user["estado"] == "menu_aguardando":
        if incoming_msg == "1":
            user["atendente"] = "👤 Atendimento solicitado"
            msg.body("📞 Legal! Já vamos chamar um atendente pra conversar com você.\n\nDigite *menu* para voltar ao menu principal.")
        elif incoming_msg == "2":
            user["tipo"] = "🎁 Teste grátis de 3 horas"
            msg.body("🎉 Você escolheu fazer um *teste grátis de 3h*!\n\nPor favor, envie agora seu *nome*, *e-mail* e *telefone* para que possamos liberar o acesso.\n\nDigite *menu* para voltar ou continue enviando seus dados.")
        elif incoming_msg == "3":
            user["estado"] = "sub_planos"
            msg.body("💳 *Nossos planos são:*\n\n"
                     "📆 *1 mês* → R$29,90\n"
                     "📆 *6 meses* → R$149,90\n"
                     "📆 *12 meses* → R$239,90\n\nTodos incluem acesso ilimitado com qualidade HD, FHD e até 4K! 🔥\n\nDigite:\n"
                     "• *1 mês*, *6 meses* ou *12 meses* para escolher\n"
                     "• *voltar* para retornar ao menu principal")
        elif incoming_msg == "4":
            msg.body("📺 Todos os nossos planos incluem acesso com qualidade de imagem excepcional:\n\n"
                     "✔️ HD\n✔️ Full HD\n✔️ 4K Ultra\n\nNada de cobranças extras! Você tem o melhor da TV, filmes e séries desde o primeiro dia. 🎉\n\nDigite *menu* para voltar.")
        elif incoming_msg == "5":
            msg.body("📩 Envie seus dados completos assim:\n\n"
                     "*Nome: Fulano da Silva*\n"
                     "*Email: fulano@homeflix.com*\n"
                     "*Telefone: (11) 91234-5678*\n"
                     "*Quero o plano de 6 meses*\n\nO sistema vai registrar tudo e montar um resumo pra você. 😊\n\nDigite *menu* para voltar.")
        elif incoming_msg == "6":
            resumo = "📋 *Resumo HOMEFLIX:*\n"
            resumo += f"👤 Nome: {user.get('nome', '❌ não informado')}\n"
            resumo += f"📧 Email: {user.get('email', '❌ não informado')}\n"
            resumo += f"📞 Telefone: {user.get('telefone', '❌ não informado')}\n"
            resumo += f"🎁 Escolha: {user.get('tipo', '❌ não informado')}\n"
            msg.body(resumo + "\n\nDigite *menu* para voltar.")
        else:
            msg.body("😅 Ops! Não entendi...\nDigite *menu* para voltar ao início ou escolha uma opção válida.")

    elif user["estado"] == "sub_planos":
        if "1 mês" in incoming_msg:
            user["tipo"] = "📆 Plano 1 mês – R$29,90"
            msg.body("✅ Plano registrado: *1 mês – R$29,90*\n\nDigite *menu* para voltar ao início.")
        elif "6 meses" in incoming_msg:
            user["tipo"] = "📆 Plano 6 meses – R$149,90"
            msg.body("✅ Plano registrado: *6 meses – R$149,90*\n\nDigite *menu* para voltar ao início.")
        elif "12 meses" in incoming_msg:
            user["tipo"] = "📆 Plano 12 meses – R$239,90"
            msg.body("✅ Plano registrado: *12 meses – R$239,90*\n\nDigite *menu* para voltar ao início.")
        elif incoming_msg == "voltar":
            user["estado"] = "menu"
            msg.body("🔙 Voltando ao menu principal...\n\nDigite *menu* para exibir as opções.")
        else:
            msg.body("❓ Não entendi... Digite *1 mês*, *6 meses*, *12 meses* ou *voltar*.")

    else:
        msg.body("🤖 Desculpe, não entendi sua mensagem.\nDigite *menu* para começar ou envie seus dados completos (nome, email, telefone e plano).")

    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
