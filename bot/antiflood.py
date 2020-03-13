import logging
import asyncio
from aiogram import Bot, exceptions


async def send_message(bot: Bot, chat_id: int, message: str):
    try:
        await bot.send_message(chat_id, message)
    except (exceptions.BotBlocked, exceptions.UserDeactivated, exceptions.ChatNotFound) as e:
        logging.debug(f'Target [ID:{chat_id}]: Impossible to reach him.')
    except exceptions.TelegramAPIError as e:
        logging.exception(f'Target [ID:{chat_id}]: Failed.')
    except exceptions.RetryAfter as e:
        logging.warning(
            f'Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.')
        await asyncio.sleep(e.timeout)
        await send_message(bot, chat_id, message)