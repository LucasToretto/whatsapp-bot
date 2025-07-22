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

    # Inicializa estrutura de usuário e estado padrão
    if from_number not in usuarios:
        usuarios[from_number] = {"estado": "menu"}

    user = usuarios[from_number]

    # Captura inteligente de dados
    nome_match = re.search(r"(meu nome é|nome:)\s*([a-zà-ÿ\'\s]+)", incoming_msg, re.IGNORECASE)
    email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", incoming_msg)
    telefone_match = re.search(r"\(?\d{2}\)?\s?\d{4,5}-?\d{4}", incoming_msg)

    if nome_match:
        user["nome"] = nome_match.group(2).strip().title()
    if email_match:
        user["email"] = email_match.group(0)
    if telefone_match:
        user["telefone"] = telefone_match.group(0)

    # Escolha do plano
    if "teste" in incoming_msg:
        user["tipo"] = "🎁 Teste grátis de 3 horas"
    elif "1 mês" in incoming_msg:
        user["tipo"] = "📆 Plano 1 mês – R$29,90"
    elif "6 meses" in incoming_msg:
        user["tipo"] = "📆 Plano 6 meses – R$149,90"
    elif "12 meses" in incoming_msg:
        user["tipo"] = "📆 Plano 12 meses – R$239,90"

    # Navegação
    if incoming_msg == "menu":
        user["estado"] = "menu"

    elif incoming_msg == "voltar":
        user["estado"] = "menu"

    # Fluxo principal
    if user["estado"] == "menu":
        msg.body("🎬 *Bem-vindo(a) à HOMEFLIX!*\n\nEscolha uma opção pra começar:\n"
                 "1️⃣ Falar com um atendente humano\n"
                 "2️⃣ Solicitar teste grátis de 3h\n"
                 "3️⃣ Ver planos disponíveis\n"
                 "4️⃣ Saber sobre qualidade de imagem\n"
                 "5️⃣ Enviar dados completos (nome, email, telefone, plano)\n"
                 "6️⃣ Ver resumo das suas escolhas\n\n👉 Digite o número da opção desejada.")
        user["estado"] = "menu_aguardando"

    elif user["estado"] == "menu_aguardando":
        if incoming_msg == "1":
            user["atendente"] = "👤 Atendimento solicitado"
            msg.body("📞 Show! Já vamos chamar um atendente pra conversar com você.\n\nDigite *menu* pra voltar ao início.")
        elif incoming_msg == "2":
            user["tipo"] = "🎁 Teste grátis de 3 horas"
            msg.body("✅ Teste registrado! Manda seu nome, email e telefone pra liberar o acesso.\n\nDigite *menu* pra voltar.")
        elif incoming_msg == "3":
            user["estado"] = "sub_planos"
            msg.body("💳 *Planos disponíveis:*\n\n"
                     "• 📆 1 mês → R$29,90\n"
                     "• 📆 6 meses → R$149,90\n"
                     "• 📆 12 meses → R$239,90\n\nIncluem HD, FHD e 4K! 🔥\n\nDigite *1 mês*, *6 meses*, *12 meses* ou *voltar*.")
        elif incoming_msg == "4":
            msg.body("📺 *Qualidade de imagem HOMEFLIX:*\n\n✔️ HD\n✔️ Full HD\n✔️ 4K Ultra\n\nTudo liberado em todos os planos!\n\nDigite *menu* pra voltar.")
        elif incoming_msg == "5":
            msg.body("📩 Pode mandar seus dados completos assim:\n\n*Nome: Fulano*\n*Email: fulano@homeflix.com*\n*Telefone: (11) 91234-5678*\n*Quero o plano de 6 meses*\n\nDigite *menu* pra voltar ou continue enviando os dados.")
        elif incoming_msg == "6":
            resumo = "📋 *Resumo HOMEFLIX:*\n"
            resumo += f"👤 Nome: {user.get('nome', '❌ não informado')}\n"
            resumo += f"📧 Email: {user.get('email', '❌ não informado')}\n"
            resumo += f"📞 Telefone: {user.get('telefone', '❌ não informado')}\n"
            resumo += f"🎁 Escolha: {user.get('tipo', '❌ não informado')}\n"
            msg.body(resumo + "\n\nDigite *menu* pra voltar ao início.")
        else:
            msg.body("😅 Ops! Não entendi essa opção...\nDigite *menu* pra recomeçar.")

    elif user["estado"] == "sub_planos":
        if "1 mês" in incoming_msg:
            user["tipo"] = "📆 Plano 1 mês – R$29,90"
            msg.body("✅ Plano registrado: *1 mês – R$29,90*\n\nDigite *menu* pra voltar.")
        elif "6 meses" in incoming_msg:
            user["tipo"] = "📆 Plano 6 meses – R$149,90"
            msg.body("✅ Plano registrado: *6 meses – R$149,90*\n\nDigite *menu* pra voltar.")
        elif "12 meses" in incoming_msg:
            user["tipo"] = "📆 Plano 12 meses – R$239,90"
            msg.body("✅ Plano registrado: *12 meses – R$239,90*\n\nDigite *menu* pra voltar.")
        elif incoming_msg == "voltar":
            user["estado"] = "menu"
            msg.body("🔙 Voltando ao menu principal...\nDigite *menu* pra exibir as opções.")
        else:
            msg.body("❓ Não reconheci esse plano. Digite *1 mês*, *6 meses*, *12 meses* ou *voltar* pra sair.")

    else:
        msg.body("🤖 Recebi sua mensagem mas não consegui interpretá-la.\n\nDigite *menu* pra recomeçar ou envie seus dados como:\n*Nome: Fulano*, *Email: fulano@...*, *Telefone: (11)...*, *Plano desejado*.")

    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
