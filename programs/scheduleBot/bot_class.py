from datetime import datetime
import requests
import telepot
import pymongo
import asyncio
import json
import os


class BotConfig:
    botKey = f"{os.getenv('ENGCOMP_TELEGRAM_TOKEN')}"
    mongoUser = f"{os.getenv('MONGO_USER')}"
    mongoPwd = f"{os.getenv('MONGO_PWD')}"
    dbName = "schedules"


class Bot:
    def __init__(self):
        self.hasSentAlert = False
        self.botConfig = BotConfig()
        self.bot = telepot.Bot(self.botConfig.botKey)
        self.client = pymongo.MongoClient(
            f"mongodb+srv://{self.botConfig.mongoUser}:{self.botConfig.mongoPwd}@cluster0.w4zli.mongodb.net/{self.botConfig.dbName}?retryWrites=true&w=majority"
        )
        self.verifySchedule()

    def convertMongoDBCursorToList(self, cursor):
        return [x for x in self.cursor]

    def createSchedule(self, info):
        db = self.client["schedules"]
        schedule_collection = db["schedule"]

        alreadyHas = False

        # verify if already exists
        for schedule in self.getScheduleList():
            if (
                schedule["message_id"] == info["message_id"]
                and schedule["chat_id"] == info["chat_id"]
            ):
                alreadyHas = True

        if alreadyHas == False:
            schedule_collection.insert_one(info)

            msg = f"Presentation scheduled by {info['scheduler']['first']} {info['scheduler']['last']}\n\n\
                {info['presentation']['theme']} \n\n\
                Presenter: {info['presentation']['presenter']}\n\n\
                date: {datetime.fromtimestamp(info['Date'])} \n\n\
                Programming Language: {info['presentation']['PL']}"

            self.bot.sendMessage(info["chat_id"], msg)
            self.verifySchedule()
            print("done")
        # else:
        #     msg = "Presentation already scheduled"
        #     self.bot.sendMessage(info["chat_id"], msg)

    def removeSchedule(self, schedule):
        print("Deleting one")
        cursor = self.getCollection()
        cursor.delete_one(
            {
                "chat_id": schedule["chat_id"],
                "message_id": schedule["message_id"],
                "Date": schedule["Date"],
            }
        )

    def getScheduleList(self):
        return self.getCollection().find()

    def getSchedulesPresentationList(self, update):
        cursor = self.getCollection()
        presentationList = cursor.find({"chat_id": update["message"]["chat"]["id"]})

        msg = ""
        for presentation in presentationList:
            presenter = presentation["presentation"]["presenter"]
            theme = presentation["presentation"]["theme"]
            date = datetime.fromtimestamp(presentation["Date"])
            msg += f"\n{presenter}: {theme} - {date}"

        self.bot.sendMessage(update["message"]["chat"]["id"], msg)

    def getCollection(self):
        db = self.client["schedules"]
        schedule_collection = db["schedule"]
        return schedule_collection

    def verifySchedule(self):
        pass
        # print("Starting verify ...")
        # db = self.client["schedules"]
        # schedule_collection = db["schedule"]
        # currentTime = datetime.now()
        # currentTime = datetime(
        #     currentTime.year,
        #     currentTime.month,
        #     currentTime.day,
        #     currentTime.hour - 3,
        #     currentTime.minute,
        # )

        # def calculateDifference(time, currentTime):
        #     time = datetime.fromtimestamp(time)
        #     dt = time - currentTime
        #     dt = dt.days * 24 * 3600 + dt.seconds
        #     if dt < 90000 and dt > 0:
        #         return 1
        #     elif dt >= 90000:
        #         return 0
        #     else:
        #         return -1

        # # verify if the diference between two timestamps is less then 1 day
        # # which means that alarm must be sent.

        # for schedule in self.getScheduleList():
        #     if (
        #         calculateDifference(schedule["Date"], currentTime) == 1
        #         and schedule["alertSent"] == False
        #     ):
        #         self.sendAlert(schedule)
        #     elif calculateDifference(schedule["Date"], currentTime) == -1:
        #         self.removeSchedule(schedule)

    def sendAlert(self, info):
        firstName = info["scheduler"]["first"]
        lastName = info["scheduler"]["last"]
        theme = info["presentation"]["theme"]
        presenter = info["presentation"]["presenter"]
        pl = info["presentation"]["PL"]
        hour = f"{datetime.fromtimestamp(info['Date']).hour}:{datetime.fromtimestamp(info['Date']).minute}"

        msg = f"There is an presentation scheduled by {firstName} {lastName} for today\n\n{theme}\n\n\nPresenter: {presenter}\nHour: {hour} \n\nProgramming Language: {pl}"

        data = {
            "chat_id": info["chat_id"],
            "question": msg,
            "is_anonymous": False,
            "options": ["Yes, i'll be there", "No i'm sorry", "Don't know yet"],
            "reply_to_message_id": info["message_id"],
        }

        response = requests.post(
            url=f"https://api.telegram.org/bot{self.botConfig.botKey}/sendPoll",
            headers={"Content-Type": "application/json"},
            data=json.dumps(data),
        )

        cursor = self.getCollection()
        cursor.find_one_and_update(
            {"message_id": info["message_id"], "chat_id": info["chat_id"]},
            {"$set": {"alertSent": True}},
        )

    def getMentions(self):
        pass

    def handleUpdates(self, updates):
        handlerTime = 120
        # updates = self.bot.getUpdates(-1)

        # for index in range(len(updates)):
        try:
            message = updates["message"]["text"]
            message_id = updates["message"]["message_id"]
            from_id = updates["message"]["from"]["id"]
            first_name = updates["message"]["from"]["first_name"]
            last_name = updates["message"]["from"]["last_name"]
            last_name = updates["message"]["from"]["last_name"]
            username = updates["message"]["from"]["username"]
            chat_id = updates["message"]["chat"]["id"]

            if len(message.upper().replace("RESERVATION:", "").split(",")) != 5:
                msg = "Please follow the pattern:\n\nreservation: date(DD/MM), hour(hh:mm), @username, programming language, theme"
                self.bot.sendMessage(chat_id, msg)
            else:
                # if dt < handlerTime:
                message = message.lower().replace("reservation:", "").split(",")
                for i in range(len(message)):
                    message[i] = message[i][1:]

                date = message[0].split("/")
                hour = message[1].split(":")
                presenter = message[2]
                Pl = message[3]
                theme = message[4]
                scheduleInfo = {
                    "Date": datetime.timestamp(
                        datetime(
                            datetime.now().year,
                            int(date[1]),
                            int(date[0]),
                            hour=int(hour[0]),
                            minute=int(hour[1]),
                        )
                    ),
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "presentation": {
                        "theme": theme,
                        "presenter": presenter,
                        "PL": Pl,
                    },
                    "scheduler": {
                        "first": first_name,
                        "last": last_name,
                    },
                    "alertSent": False,
                }
                self.createSchedule(scheduleInfo)

        # self.bot.sendMessage(chat_id, message, reply_to_message_id=message_id)
        except:
            pass
