import os


def setConfig():
    # Set environment variables
    # Telegram
    os.environ["SENDMAN_TELEGRAM_TOKEN"] = "TELEGRAM_TOKEN"
    os.environ["ENGCOMP_TELEGRAM_TOKEN"] = "TELEGRAM_TOKEN"
    os.environ["CALDERARO_TELEGRAM_CHAT_ID"] = CHAT_ID
    os.environ["GALENDE_TELEGRAM_CHAT_ID"] = CHAT_ID
    os.environ["HEYDRIGH_TELEGRAM_CHAT_ID"] = CHAT_ID
    os.environ["MONGO_USER"] = "USER_MONGO"
    os.environ["MONGO_PWD"] = "USER_PASSWORD"
