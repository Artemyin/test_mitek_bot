from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from os import mkdir, environ
from os.path import exists
from dotenv import load_dotenv
from crud import create_photo, create_user, get_user_by_id, create_voice
import json
import boto3

from worker import celery

load_dotenv(".env")

BOT_TOKEN = environ.get("BOT_TOKEN")

s3 = boto3.client('s3',
                  aws_access_key_id=environ.get("AWS_ACCESS_KEY_ID"),
                  aws_secret_access_key=environ.get("AWS_SECRET_ACCESS_KEY")
                  )
bucket_name = environ.get("BUCKET_NAME")


def add_user_photo(user, file_name):
    if not get_user_by_id(user.id):  # move this part into decorator?
        create_user(user.id, user.username)
    create_photo(user.id, file_name)


def add_user_voice(user, file_name):
    # user.id - unique telegram user id
    if not get_user_by_id(user.id):  # move this part into decorator?
        create_user(user.id, user.username)
    create_voice(user.id, file_name)


class PhotoVoiceBot:

    def __init__(self, bot_token):
        self.bot = Bot(bot_token)
        self.voices_folder = "voices"
        self.photos_folder = "photos"
        for folder in (self.voices_folder, self.photos_folder):
            if not exists(folder):
                mkdir(folder, mode=0o777)

    async def get_file(self, obj):
        file_id = obj.file_id
        return await self.bot.get_file(file_id)

    async def hello(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f"Hello {update.effective_user.first_name}")

    async def download_user_photos(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = update.message
        user = message.from_user
        photo = message.photo[-1]  # replace with ENUM ?

        photo_id = photo.file_id
        voice_file = await self.get_file(photo)
        photo_link = voice_file.file_path

        task = celery.send_task('process_photo', args=[photo_link, photo_id, user.id], kwargs={})
        await message.reply_text(f"create task")
        task_id = task.id
        work = celery.AsyncResult(task_id)
        result = work.get()
        await message.reply_text(f"get result")

        downloaded_file = result.get("result")
        add_user_photo(user, downloaded_file)

        await message.reply_text(f"Photos from user {user.id} was saved {downloaded_file}")
        await message.reply_text(f"{json.dumps(result, indent=2)}")

    async def download_user_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = update.message
        user = message.from_user
        voice = message.voice

        voice_id = voice.file_id
        voice_file = await self.get_file(voice)
        voice_link = voice_file.file_path

        task = celery.send_task('process_voice', args=[voice_link, voice_id, user.id], kwargs={})
        await message.reply_text(f"create task")
        task_id = task.id
        work = celery.AsyncResult(task_id)
        result = work.get()
        await message.reply_text(f"get result")

        downloaded_file = result.get("result")
        add_user_voice(user, downloaded_file)

        print(f"voice message from user {message.from_user.id} was saved")

        await message.reply_text(f"voice message {downloaded_file} from user {message.from_user.id} was saved")


bot_access = PhotoVoiceBot(BOT_TOKEN)
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("hello", bot_access.hello))
app.add_handler(MessageHandler(filters.VOICE, bot_access.download_user_voice))
app.add_handler(MessageHandler(filters.PHOTO, bot_access.download_user_photos))

app.run_polling()


