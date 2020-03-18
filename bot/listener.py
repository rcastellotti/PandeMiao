import settings
import utils.dbmigration
import handlers.start
from aiogram import Bot, Dispatcher, executor, types
from neo4j import GraphDatabase


# Initialize db link
db_auth = (settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD)
db = GraphDatabase.driver(settings.NEO4J_URI,
                          auth=db_auth,
                          encrypted=settings.NEO4J_ENCRYPTED)
utils.dbmigration.migrate(db)

# Initialize bot and dispatcher
bot = Bot(token=settings.TELEGRAM_API_TOKEN)
dp = Dispatcher(bot)


# Handlers
@dp.message_handler(commands=['start'])  # type: ignore
async def start_handler(message: types.Message) -> None:
    await handlers.start.handle(message)


@dp.message_handler(commands=['victims'])  # type: ignore
async def victims_handler(message: types.Message) -> None:
    await message.reply('Non hai ancora contagiatto nessuno 🐈')


@dp.message_handler(commands=['dumpmydata'])  # type: ignore
async def dumpmydata_handler(message: types.Message) -> None:
    await message.reply('Come pretendi un gatto conosca qualcosa di te? 😺')


@dp.message_handler(commands=['forgetaboutme'])  # type: ignore
async def forgetaboutme_handler(message: types.Message) -> None:
    await message.reply("Don't you, forget about me \n"
                        "Don't, don't, don't, don't  😿")


@dp.message_handler(commands=['help'])  # type: ignore
async def help_handler(message: types.Message) -> None:
    await message.reply('Hey ciao! Sono PandeMiao, '
                        'un progetto tutto open '
                        'che simula il propagarsi di una epidemia. '
                        'Se vuoi sapere come sono fatto '
                        'puoi trovare il mio codice su '
                        'https://github.com/rage-against-the-data/PandeMiao/')


# Polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
    db.close()
