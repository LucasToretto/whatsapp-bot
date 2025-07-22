from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()

    if "oi" in incoming_msg:
        msg.body("Olá! 👋 Como posso te ajudar hoje?")
    elif "horário" in incoming_msg:
        msg.body("Nosso horário de atendimento é das 9h às 18h.")
    else:
        msg.body("Desculpe, não entendi. Pode repetir?")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)