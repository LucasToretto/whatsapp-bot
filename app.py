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

    # 👤 Inicializa estado do usuário
    if from_number not in usuarios:
        usuarios[from_number] = {"estado": "menu"}

    user = usuarios[from_number]

    # ✍️ Captura de dados (nome, email, telefone)
    nome_match = re.search(r"(meu nome é|nome:)\s*([a-zà-ÿ\'\s]+)", incoming_msg, re.IGNORECASE)
    email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", incoming_msg)
    telefone_match = re.search(r"\(?\d{2}\)?\s?\d{4,5}-?\d{4}", incoming_msg)

    if nome_match:
        user["nome"] = nome_match.group(2).strip().title()
    if email_match:
        user["email"] = email_match.group(0)
    if telefone_match:
        user["telefone"] = telefone_match.group(0)

    # 🎯 Detecção de intenção (planos ou teste)
    if "teste" in incoming_msg:
        user["tipo"] = "🎁 Teste gratuito de 3 horas"
    elif "1 mês" in incoming_msg:
        user["tipo"] = "📅 Plano 1 mês – R$29,90"
    elif "6 meses" in incoming_msg:
        user["tipo"] = "📅 Plano 6 meses – R$149,90"
    elif "12 meses" in incoming_msg:
        user["tipo"] = "📅 Plano 12 meses – R$239,90"

    # 🔄 Navegação
    if incoming_msg == "menu":
        user["estado"] = "menu"
    elif incoming_msg == "voltar":
        user["estado"] = "menu"

    # 🎬 Menu principal
    if user["estado"] == "menu":
        msg.body("👋 *E aí! Eu sou o HomeBot, seu guia na terra das séries e filmes infinitos.*\n\nEscolhe o que você quer maratonar agora:\n"
                 "1️⃣ Falar com um atendente humano (sim, de carne e osso 😎)\n"
                 "2️⃣ Testar por 3 horinhas grátis 🎁\n"
                 "3️⃣ Ver os planos que até o Sheldon aprovaria 💳\n"
                 "4️⃣ Saber da qualidade das imagens (spoiler: é de cinema 🎥)\n"
                 "5️⃣ Me mandar seus dados de uma vez 📝\n"
                 "6️⃣ Ver o resumo da sua jornada até aqui 📋\n\n👉 Digita o número e vamos nessa!")
        user["estado"] = "menu_aguardando"

    elif user["estado"] == "menu_aguardando":
        if incoming_msg == "1":
            user["atendente"] = "👤 Atendimento solicitado"
            msg.body("📞 Chamei o atendente! Enquanto ele chega, que tal escolher seu plano dos sonhos?\n\nDigite *menu* pra voltar.")
        elif incoming_msg == "2":
            user["tipo"] = "🎁 Teste gratuito de 3 horas"
            msg.body("✅ Teste ativo! Manda aí seu *nome*, *e-mail* e *telefone* — ou como diria o Tony Stark: ‘deixe-me ver o que você tem aí’. 🦾\n\nDigite *menu* pra voltar.")
        elif incoming_msg == "3":
            user["estado"] = "sub_planos"
            msg.body("💳 *Planos HOMEFLIX™* — tão bons que até o Netflix tá pensando em copiar:\n\n"
                     "📆 *1 mês* → R$29,90\n"
                     "📆 *6 meses* → R$149,90\n"
                     "📆 *12 meses* → R$239,90\n\nTodos com HD, FHD e 4K liberados! 🔥\n\nDigite *1 mês*, *6 meses*, *12 meses* ou *voltar*.")
        elif incoming_msg == "4":
            msg.body("🎥 Qualidade da imagem? Mais nítida que plot twist de série britânica:\n\n✔️ HD\n✔️ Full HD\n✔️ 4K Ultra — só não fazemos café, ainda ☕\n\nDigite *menu* pra voltar.")
        elif incoming_msg == "5":
            msg.body("📝 Manda seus dados no estilo ficha de personagem, assim:\n\n*Nome: Maria das Séries*\n*Email: maria@homeflix.com*\n*Telefone: (11) 91234-5678*\n*Quero o plano de 6 meses*\n\nDigite *menu* pra voltar ou continue mandando os dados.")
        elif incoming_msg == "6":
            resumo = "📋 *Resumo do seu rolê pelo HOMEFLIX:*\n"
            resumo += f"👤 Nome: {user.get('nome', '❌ ainda não sei')}\n"
            resumo += f"📧 Email: {user.get('email', '❌ cadê o e-mail?')}\n"
            resumo += f"📞 Telefone: {user.get('telefone', '❌ me manda, vai')}\n"
            resumo += f"🎁 Escolha: {user.get('tipo', '❌ nada por aqui')}\n"
            msg.body(resumo + "\n\n🍿 Tá tudo aí! Digite *menu* pra voltar pro trailer da conversa.")
        else:
            msg.body("😬 Essa opção não tava no script... Digita *menu* pra recomeçar ou *voltar* pra dar aquela espiada nos planos.")

    elif user["estado"] == "sub_planos":
        if "1 mês" in incoming_msg:
            user["tipo"] = "📆 Plano 1 mês – R$29,90"
            msg.body("✅ Plano de 1 mês salvo! Esse é tipo episódio piloto: rápido, barato e viciante.\n\nDigite *menu* pra voltar.")
        elif "6 meses" in incoming_msg:
            user["tipo"] = "📆 Plano 6 meses – R$149,90"
            msg.body("✅ Meio ano de maratonas garantido! Isso sim é binge-watching profissional 😎\n\nDigite *menu* pra voltar.")
        elif "12 meses" in incoming_msg:
            user["tipo"] = "📆 Plano 12 meses – R$239,90"
            msg.body("✅ Um ano inteiro de sofá, pipoca e episódios infinitos... Netflix que se cuide! 🍿\n\nDigite *menu* pra voltar.")
        elif incoming_msg == "voltar":
            user["estado"] = "menu"
            msg.body("🔙 Voltando pro menu... tipo voltar pro início da temporada. Digite *menu* pra ver as opções.")
        else:
            msg.body("🤔 Não reconheci essa resposta. Escolha *1 mês*, *6 meses*, *12 meses* ou *voltar* pra fugir dos spoilers.")

    else:
        msg.body("👀 Ei, ainda tô tentando entender...\nTalvez você tenha digitado algo fora do script 🤖\n\n👉 Digita *menu* pra começar de novo ou manda seus dados estilo ficha técnica!")

    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
