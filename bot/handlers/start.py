from aiogram import types


async def handle(message: types.Message) -> None:
    message_parts = message.text.split(' ')

    if len(message_parts) < 2:
        await message.reply('Hey, sono una miaolattia pericolosa 😼')
        return

    patient_id = message_parts[1]  # Get param
    await handler_from_patient(message, patient_id)


async def handler_from_patient(message: types.Message, patient_id: str) -> None:
    await message.reply('Sei stato contagiatto da {} 😼'.format(patient_id))
