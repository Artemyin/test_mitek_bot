from os import environ
from dotenv import load_dotenv
import json

from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from worker import celery

from crud import add_user_photo, add_user_voice

load_dotenv(".env")

BOT_TOKEN = environ.get("BOT_TOKEN")


class PhotoVoiceBot:

    def __init__(self, bot_token):
        self.bot = Bot(bot_token)

    async def get_file(self, obj):
        file_id = obj.file_id
        return await self.bot.get_file(file_id)

    @staticmethod
    def create_work(**kwargs):
        link = kwargs.get("link")
        file_id = kwargs.get("file_id")
        user_id = kwargs.get("user_id")
        task = celery.send_task('process_voice', args=[link, file_id, user_id], kwargs={})
        task_id = task.id
        work = celery.AsyncResult(task_id)
        return work.get()

    async def hello(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f"Hello {update.effective_user.first_name}")

    async def download_user_photos(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = update.message
        user = message.from_user
        photo = message.photo[-1]  # replace with ENUM ?

        photo_id = photo.file_id
        voice_file = await self.get_file(photo)
        photo_link = voice_file.file_path

        result = self.create_work(link=photo_link, file_id=photo_id, user_id=user.id)

        downloaded_file = result.get("result")
        if not downloaded_file:
            await message.reply_text(f"Photos from user {user.id} cant recognize face")
            return
        add_user_photo(user=user, file_name=downloaded_file)

        await message.reply_text(f"Photos from user {user.id} was saved {downloaded_file}")
        await message.reply_text(f"{json.dumps(result, indent=2)}")

    async def download_user_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = update.message
        user = message.from_user
        voice = message.voice

        voice_id = voice.file_id
        voice_file = await self.get_file(voice)
        voice_link = voice_file.file_path

        result = self.create_work(link=voice_link, file_id=voice_id, user_id=user.id)

        downloaded_file = result.get("result")
        add_user_voice(user=user, file_name=downloaded_file)

        print(f"voice message from user {message.from_user.id} was saved")

        await message.reply_text(f"voice message {downloaded_file} from user {message.from_user.id} was saved")


bot_access = PhotoVoiceBot(BOT_TOKEN)
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("hello", bot_access.hello))
app.add_handler(MessageHandler(filters.VOICE, bot_access.download_user_voice))
app.add_handler(MessageHandler(filters.PHOTO, bot_access.download_user_photos))

app.run_polling()

