'''Handler of incoming messages.'''

import logging
from aiogram import Bot, Dispatcher, executor, types, exceptions
from aiogram.utils.deep_linking import get_start_link
from neo4j import Driver
import settings
import utils.queries as queries
from utils.dbinit import db_connect


# Init the db
DB: Driver = db_connect(retry=5, wait_sec=5)

# Init bot and dispatcher
BOT = Bot(token=settings.TELEGRAM_API_TOKEN)
DP = Dispatcher(BOT)


# Handlers
@DP.message_handler(commands=['start'])  # type: ignore
async def start_handler(message: types.Message) -> None:
    '''Show a welcome message and a start_link to infect people.'''

    from_chat_id = message.from_user.id
    start_referrer = message.get_args()

    if not start_referrer:
        new_referrer = queries.set_infected(DB, from_chat_id)
    else:
        new_referrer = queries.set_infected_from(
            DB, from_chat_id, start_referrer)

    start_link: str = await get_start_link(new_referrer)

    try:
        await message.reply('Hey, sono una miaolattia pericolosa 😼\n' +
                            'Per contagiare i tuoi (a)mici ' +
                            'inviagli questo link:\n' +
                            start_link)
    except exceptions.TelegramAPIError as exc:
        logging.exception('Target [ID:%s]: %s.', from_chat_id, str(exc))


@DP.message_handler(commands=['victims'])  # type: ignore
async def victims_handler(message: types.Message) -> None:
    '''Reply with a count of your victims.'''

    await message.reply('Non hai ancora contagiatto nessuno 🐈')


@DP.message_handler(commands=['dumpmydata'])  # type: ignore
async def dumpmydata_handler(message: types.Message) -> None:
    '''Reply with data that belongs to you.'''

    await message.reply('Come pretendi un gatto conosca qualcosa di te? 😺')


@DP.message_handler(commands=['forgetaboutme'])  # type: ignore
async def forgetaboutme_handler(message: types.Message) -> None:
    '''Ask you to confirm the removal of your data.'''

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.row(
        types.InlineKeyboardButton('No', callback_data='forgetaboutme:no'),
        types.InlineKeyboardButton("Si", callback_data='forgetaboutme:yes')
    )

    await message.reply('Non voglio dimenticarti 😿\n' +
                        'Se vuoi solo smettere di ricevere le notifiche, ' +
                        'cancella questa chat.\n' +
                        'Sei sicuro di voler cancellare i tuoi dati? ' +
                        'Tutti i tuoi progressi andranno persi',
                        reply_markup=keyboard)


@DP.callback_query_handler(text='forgetaboutme:no')  # type: ignore
async def forgetaboutme_no_handler(
        query: types.CallbackQuery) -> None:
    '''Remove messages if you don't want to delete data.'''

    await query.answer()
    await BOT.delete_message(query.from_user.id,
                             query.message.message_id)
    await BOT.delete_message(query.from_user.id,
                             query.message.reply_to_message.message_id)


@DP.callback_query_handler(text='forgetaboutme:yes')  # type: ignore
async def forgetaboutme_yes_handler(query: types.CallbackQuery) -> None:
    '''Delete your personal data.'''

    await query.answer()
    # TODO: Anonimyze data
    await BOT.send_message(query.from_user.id, ':( Adieu')


@DP.message_handler(commands=['help'])  # type: ignore
async def help_handler(message: types.Message) -> None:
    '''Send you infos about the project.'''

    await message.reply('Hey ciao! Sono PandeMiao, '
                        'un progetto tutto open '
                        'che simula il propagarsi di una epidemia. '
                        'Se vuoi sapere come sono fatto '
                        'puoi trovare il mio codice su '
                        'https://github.com/rage-against-the-data/PandeMiao/')


# Wait messages and close the db at the end
executor.start_polling(DP, skip_updates=False)
DB.close()
