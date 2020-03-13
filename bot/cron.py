import settings
import antiflood
import asyncio
from aiogram import Bot, Dispatcher, executor


async def daily_update():
    await antiflood.send_message(bot, settings.ADMIN_USER_ID, 'Cron job started')

    # Notify all users
    for i in range(2):
        message = 'meow ' + str(i)
        await antiflood.send_message(bot, settings.ADMIN_USER_ID, message)
        await asyncio.sleep(1.0)  # Max 1 message / sec

    await antiflood.send_message(bot, settings.ADMIN_USER_ID, 'Cron job ended')


# Initialize bot
bot = Bot(token=settings.TELEGRAM_API_TOKEN)
dp = Dispatcher(bot)

if __name__ == '__main__':
    executor.start(dp, daily_update())
