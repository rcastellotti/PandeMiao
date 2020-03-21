import logging
import asyncio
from aiogram import Bot, exceptions


async def send_message(message: str, chat_id: int,
                       bot: Bot, silent: bool = False) -> None:
    try:
        await bot.send_message(chat_id, message, disable_notification=silent)

    except (exceptions.BotBlocked,
            exceptions.UserDeactivated,
            exceptions.ChatNotFound):
        logging.debug(f'Target [ID:{chat_id}]: Impossible to reach him.')

    except exceptions.TelegramAPIError:
        logging.exception(f'Target [ID:{chat_id}]: Failed.')
