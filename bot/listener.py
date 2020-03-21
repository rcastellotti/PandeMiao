import settings
import logging
import utils.queries as queries
import utils.dbmigration as dbmigration
from aiogram import Bot, Dispatcher, executor, types, exceptions
from aiogram.utils.deep_linking import get_start_link
from neo4j import GraphDatabase


# Initialize db link
db_auth = (settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD)
db = GraphDatabase.driver(settings.NEO4J_URI,
                          auth=db_auth,
                          encrypted=settings.NEO4J_ENCRYPTED)
dbmigration.migrate(db)

# Initialize bot and dispatcher
bot = Bot(token=settings.TELEGRAM_API_TOKEN)
dp = Dispatcher(bot)


# Handlers
@dp.message_handler(commands=['start'])  # type: ignore
async def start_handler(message: types.Message) -> None:
    from_chatID = message.from_user.id
    start_referrer = message.get_args()

    if not start_referrer:
        new_referrer = queries.set_infected(db, from_chatID)
    else:
        new_referrer = queries.set_infected_from(
            db, from_chatID, start_referrer)

    start_link: str = await get_start_link(new_referrer)

    try:
        await message.reply('Hey, sono una miaolattia pericolosa 😼\n' +
                            'Hai 7 giorni per contagiare i tuoi (a)mici ' +
                            'inviandogli questo link:\n' +
                            start_link)
    except exceptions.TelegramAPIError as e:
        logging.exception(f'Target [ID:{from_chatID}]: {str(e)}.')


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
