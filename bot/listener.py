import settings
import handlers.start
from aiogram import Bot, Dispatcher, executor, types


# Initialize bot and dispatcher
bot = Bot(token=settings.TELEGRAM_API_TOKEN)
dp = Dispatcher(bot)


# Handlers
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await handlers.start.handle(message)


@dp.message_handler(commands=['victims'])
async def victims_handler(message: types.Message):
    await message.reply('Non hai ancora contagiatto nessuno 🐈')


@dp.message_handler(commands=['dumpmydata'])
async def dumpmydata_handler(message: types.Message):
    await message.reply('Come pretendi un gatto conosca qualcosa di te? 😺')


@dp.message_handler(commands=['forgetaboutme'])
async def forgetaboutme_handler(message: types.Message):
    await message.reply("Don't you, forget about me \nDon't, don't, don't, don't  😿")


@dp.message_handler(commands=['help'])
async def forgetaboutme_handler(message: types.Message):
    await message.reply('Hey ciao, sono PandeMiao, un progetto tutto open che simula il propagarsi di una epidemia. Se vuoi sapere come sono fatto puoi trovare il mio codice su https://github.com/rage-against-the-data/PandeMiao/')


# Polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)