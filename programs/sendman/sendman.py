import os


class chatIds:
    calderaro = int(os.getenv("CALDERARO_TELEGRAM_CHAT_ID"))
    galende = int(os.getenv("GALENDE_TELEGRAM_CHAT_ID"))
    heydrigh = int(os.getenv("HEYDRIGH_TELEGRAM_CHAT_ID"))


def send(id, message, botInstance):
    botInstance.sendMessage(chat_id=id, text=message)
