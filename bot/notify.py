import settings
import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, exceptions


async def daily_update() -> None:
    # TODO: Notify all users
    for i in range(2):
        chat_id = 844457200
        message = 'meow ' + str(i)
        await send_message(chat_id, message)


async def send_message(chat_id: int, message: str) -> None:
    try:
        await bot.send_message(chat_id=chat_id,
                               text=message, disable_notification=True)
        await asyncio.sleep(1.0)  # Max 1 message / sec

    except (exceptions.BotBlocked,
            exceptions.UserDeactivated,
            exceptions.ChatNotFound):
        logging.debug(f'Target [ID:{chat_id}]: Impossible to reach him.')

    except exceptions.TelegramAPIError as e:
        logging.exception(f'Target [ID:{chat_id}]: {str(e)}.')


# Initialize bot
bot = Bot(token=settings.TELEGRAM_API_TOKEN)
dp = Dispatcher(bot)

if __name__ == '__main__':
    executor.start(dp, daily_update())
