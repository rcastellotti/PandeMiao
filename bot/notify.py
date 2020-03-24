'''Notify users of how many people they have infected.'''

import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, exceptions
import settings

# Init bot and dispatcher
BOT = Bot(token=settings.TELEGRAM_API_TOKEN)
DP = Dispatcher(BOT)


async def daily_update() -> None:
    # TODO: Notify all users
    for i in range(2):
        chat_id = 844457200
        message = 'meow ' + str(i)
        await send_message(chat_id, message)


async def send_message(chat_id: int, message: str) -> None:
    '''Send a message to a single user.'''

    try:
        await BOT.send_message(chat_id=chat_id,
                               text=message, disable_notification=True)
        await asyncio.sleep(1.0)  # Max 1 message / sec

    except (exceptions.BotBlocked,
            exceptions.UserDeactivated,
            exceptions.ChatNotFound):
        logging.debug(f'Target [ID:{chat_id}]: Impossible to reach him.')

    except exceptions.TelegramAPIError as exc:
        logging.exception(f'Target [ID:{chat_id}]: {str(exc)}.')


# Send messages
executor.start(DP, daily_update())
