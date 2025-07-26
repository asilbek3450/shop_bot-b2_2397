import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN, ADMINS
from handlers.register import register_start_handler
from handlers.admin import register_category_handlers, register_product_handlers
from handlers.users import register_menu_handlers
from database import create_tables, add_user, search_user_by_id

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)
from keyboards import admin_keyboard, user_keyboard, register_keyboard

@dp.message(Command("start"))
async def start_handler(message: Message):
    user_id = message.from_user.id # type: ignore

    if user_id in ADMINS:  # adminlar ID ro'yxati
        await message.answer("Assalomu alaykum, admin!", reply_markup=admin_keyboard)
    else:
        if search_user_by_id(user_id):  # bajarishila kere
            await message.answer("Assalomu alaykum, foydalanuvchi!", reply_markup=user_keyboard)
        else:
            await message.answer("Siz hali ro'yhatdan o'tmagansiz! 👇", reply_markup=register_keyboard)
  
register_start_handler(dp=dp)
register_category_handlers(dp=dp)
register_product_handlers(dp=dp)
register_menu_handlers(dp=dp)

async def main():
    create_tables()  # bazani yaratish
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
