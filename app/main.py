from telegram import Update, Bot, Voice, PhotoSize
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from pathlib import Path
from os import mkdir, environ
from os.path import exists
from dotenv import load_dotenv
from crud import create_photo, create_user, get_user_by_id, create_voice
import json

import celery.states as states
from worker import celery
# from celery_queue.celery_worker import create_task, process_photo


def add_user_photo(user, file_name):
    if not get_user_by_id(user.id):  # move this part into decorator?
        create_user(user.id, user.username)
    create_photo(user.id, file_name)

def add_user_voice(user, file_name):
    if not get_user_by_id(user.id):  # move this part into decorator?
        create_user(user.id, user.username)
    create_voice(user.id, file_name)


load_dotenv(".env")

BOT_TOKEN = environ["BOT_TOKEN"]

class BotMixin:
    async def download_object(self, obj):
        obj_file = await self.get_file(obj)
        print(f"got photo file {obj_file}")
        file_link = obj_file.file_path
        file_name = await self.download_file(obj_file, obj)
        return file_name, file_link
        # print(f"Photos from user {obj_file.file_unique_id} was downloaded")


    async def get_file(self, obj):
        file_id = obj.file_id
        return await self.bot.get_file(file_id)

    async def download_file(self, file, obj):
        if isinstance(obj, PhotoSize):
            folder = self.photos_folder
        if isinstance(obj, Voice):
            folder = self.voices_folder
        # str(uuid.uuid4())
        file_path = Path.cwd().joinpath(folder, file.file_unique_id)
        await file.download_to_drive(file_path)
        return file.file_unique_id

class PhotoVoiceBot(BotMixin):

    def __init__(self, bot_token):
        self.bot = Bot(bot_token)
        self.voices_folder = "voices"
        self.photos_folder = "photos"
        for folder in (self.voices_folder, self.photos_folder):
            if not exists(folder):
                mkdir(folder, mode=0o777)

    async def hello(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f"Hello {update.effective_user.first_name}")

    async def download_user_photos(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = update.message
        user = message.from_user
        photo = message.photo[-1]  # replace with ENUM ?
        photo_name, link = await self.download_object(photo)
        print(f"Photos from user {user.id} was saved")

        task = celery.send_task('process_photo', args=[link], kwargs={})
        task_id = task.id
        work = celery.AsyncResult(task_id)
        result = work.get()

        add_user_photo(user, photo_name)

        await message.reply_text(f"Photos from user {user.id} was saved {link}")
        await message.reply_text(f"{json.dumps(result, indent=2)}")

    async def download_user_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = update.message
        user = message.from_user
        voice = message.voice

        voice_name = await self.download_object(voice)
        add_user_voice(user, voice_name)

        print(f"voice message from user {message.from_user.id} was saved")

        await message.reply_text(f"voice message from user {message.from_user.id} was saved")


    async def run_task(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        amount = 1
        x = 2
        y = 3
        print("Inside task")
        task = celery.send_task('create_task', args=[amount, x, y], kwargs={})
        task_id = task.id
        work = celery.AsyncResult(task_id)
        result = work.get()
        print("task sent")
        await update.message.reply_text(f"task execute: {result}")


bot_access = PhotoVoiceBot(BOT_TOKEN)
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("hello", bot_access.hello))
app.add_handler(CommandHandler("task", bot_access.run_task))
app.add_handler(MessageHandler(filters.VOICE, bot_access.download_user_voice))
app.add_handler(MessageHandler(filters.PHOTO, bot_access.download_user_photos))

app.run_polling()


