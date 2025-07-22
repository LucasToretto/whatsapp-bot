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

    # Inicializa usuário com estado padrão
    if from_number not in usuarios:
        usuarios[from_number] = {"estado": "menu"}

    user = usuarios[from_number]

    # Captura automática de dados enviados
    nome_match = re.search(r"(meu nome é|nome:)\s*([a-zà-ÿ\'\s]+)", incoming_msg, re.IGNORECASE)
    email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", incoming_msg)
    telefone_match = re.search(r"\(?\d{2}\)?\s?\d{4,5}-?\d{4}", incoming_msg)

    if nome_match:
        user["nome"] = nome_match.group(2).strip().title()
    if email_match:
        user["email"] = email_match.group(0)
    if telefone_match:
        user["telefone"] = telefone_match.group(0)

    # Identifica plano ou teste
    if "teste" in incoming_msg:
        user["tipo"] = "🎁 Teste gratuito de 3 horas"
    elif "1 mês" in incoming_msg:
        user["tipo"] = "📅 Plano 1 mês – R$29,90"
    elif "6 meses" in incoming_msg:
        user["tipo"] = "📅 Plano 6 meses – R$149,90"
    elif "12 meses" in incoming_msg:
        user["tipo"] = "📅 Plano 12 meses – R$239,90"

    # Comandos de navegação
    if incoming_msg == "menu":
        user["estado"] = "menu"
    elif incoming_msg == "voltar":
        user["estado"] = "menu"

    # Menu principal
    if user["estado"] == "menu":
        msg.body("👋 *E aí! Eu sou o HomeBot, seu guia oficial nas maratonas da HOMEFLIX.*\n\nEscolha uma opção pra começar:\n"
                 "1️⃣ Falar com atendente humano 😎\n"
                 "2️⃣ Solicitar teste grátis 🎁\n"
                 "3️⃣ Ver planos disponíveis 💳\n"
                 "4️⃣ Qualidade de imagem 📺\n"
                 "5️⃣ Enviar seus dados 📝\n"
                 "6️⃣ Ver resumo do seu atendimento 📋\n\nDigite o número da opção desejada.")
        user["estado"] = "menu_aguardando"

    elif user["estado"] == "menu_aguardando":
        if incoming_msg == "1":
            user["atendente"] = "👤 Atendimento solicitado"
            msg.body("📞 Um atendente foi acionado e já deve estar a caminho!\n\nDigite *menu* pra voltar ao menu principal.")
        elif incoming_msg == "2":
            user["tipo"] = "🎁 Teste gratuito de 3 horas"
            msg.body("✅ Show! Teste de 3h ativado. Agora me manda seu *nome*, *email* e *telefone* pra liberar o acesso. 😄\n\nDigite *menu* pra voltar.")
        elif incoming_msg == "3":
            user["estado"] = "sub_planos"
            msg.body("💳 *Planos HOMEFLIX* disponíveis:\n\n"
                     "📆 *1 mês* → R$29,90\n"
                     "📆 *6 meses* → R$149,90\n"
                     "📆 *12 meses* → R$239,90\n\nCom direito a HD, FHD e 4K liberado! 🔥\n\nDigite o plano desejado ou *voltar* pra retornar ao menu.")
        elif incoming_msg == "4":
            msg.body("📺 Imagens mais nítidas que revelação de série:\n\n✔️ HD\n✔️ Full HD\n✔️ 4K Ultra\n\nTudo disponível em qualquer plano!\n\nDigite *menu* pra voltar.")
        elif incoming_msg == "5":
            msg.body("📝 Me envie seus dados num único texto assim:\n\n*Nome: Fulano da Série*\n*Email: fulano@homeflix.com*\n*Telefone: (11) 91234-5678*\n*Quero o plano de 6 meses*\n\nO HomeBot vai interpretar tudo! 😎 Digite *menu* se quiser voltar.")
        elif incoming_msg == "6":
            resumo = "📋 *Seu resumo com o HomeBot:*\n"
            resumo += f"👤 Nome: {user.get('nome', '❌ não informado')}\n"
            resumo += f"📧 Email: {user.get('email', '❌ não informado')}\n"
            resumo += f"📞 Telefone: {user.get('telefone', '❌ não informado')}\n"
            resumo += f"🎁 Escolha: {user.get('tipo', '❌ não informado')}\n"
            msg.body(resumo + "\n\n🍿 Quando quiser voltar pro menu, é só digitar *menu*!")
        else:
            msg.body("😬 Opa! Essa opção não tá no catálogo… Digita *menu* pra ver as opções ou *voltar* pra onde estava.")

    elif user["estado"] == "sub_planos":
        if "1 mês" in incoming_msg:
            user["tipo"] = "📆 Plano 1 mês – R$29,90"
            msg.body("✅ Plano registrado: *1 mês – R$29,90*\n\n🍿 Digite *menu* pra explorar outras opções.")
        elif "6 meses" in incoming_msg:
            user["tipo"] = "📆 Plano 6 meses – R$149,90"
            msg.body("✅ Plano registrado: *6 meses – R$149,90*\n\n🔥 Digite *menu* pra voltar ao menu principal.")
        elif "12 meses" in incoming_msg:
            user["tipo"] = "📆 Plano 12 meses – R$239,90"
            msg.body("✅ Plano registrado: *12 meses – R$239,90*\n\n🎬 Digite *menu* pra continuar navegando.")
        elif incoming_msg == "voltar":
            user["estado"] = "menu"
            msg.body("🔙 De volta ao menu principal!\n\nDigite *menu* pra exibir as opções.")
        else:
            msg.body("🤔 Não encontrei esse plano no catálogo. Digite *1 mês*, *6 meses*, *12 meses* ou *voltar*.")

    else:
        msg.body("🤖 Recebi sua mensagem, mas não consegui entender.\nTente digitar *menu* pra começar ou envie seus dados como:\n*Nome:...*, *Email:...*, *Telefone:...*, *Plano desejado*.")

    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
