import os
import time
import json
import urllib.request

TOKEN = os.environ["BOT_TOKEN"]
URL = f"https://api.telegram.org/bot{TOKEN}/"

def enviar(chat_id, mensagem):
    dados = json.dumps({
        "chat_id": chat_id,
        "text": mensagem
    }).encode()

    req = urllib.request.Request(
        URL + "sendMessage",
        data=dados,
        headers={"Content-Type": "application/json"}
    )

    urllib.request.urlopen(req)

offset = 0

while True:
    try:
        req = urllib.request.urlopen(
            URL + f"getUpdates?offset={offset}&timeout=30"
        )
        dados = json.loads(req.read())

        for update in dados["result"]:
            offset = update["update_id"] + 1
            msg = update.get("message", {})
            chat = msg.get("chat", {})
            texto = msg.get("text", "")

            if texto == "/start":
                enviar(
                    chat["id"],
                    "TradeVision iniciado! 📊\n"
                    "Use /teste para testar os alertas."
                )

            elif texto == "/teste":
                enviar(
                    chat["id"],
                    "🟡 ALERTA DE DEMONSTRAÇÃO\n"
                    "Possível oportunidade detectada.\n"
                    "Nenhuma operação real foi analisada."
                )

        time.sleep(1)

    except Exception as erro:
        print("Erro:", erro)
        time.sleep(5)