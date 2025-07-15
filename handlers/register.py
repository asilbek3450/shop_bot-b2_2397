from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import RegisterStates
from keyboards import phone_keyboard
from config import ADMINS
from aiogram import Dispatcher
from database import add_user, search_user_by_id

async def start_registration(message: Message, state: FSMContext):
    await message.answer("👤 Iltimos, ismingizni kiriting:")
    await state.set_state(RegisterStates.ism)

async def get_name(message: Message, state: FSMContext):
    await state.update_data(ism=message.text)
    await message.answer("📱 Endi telefon raqamingizni yuboring:", reply_markup=phone_keyboard)
    await state.set_state(RegisterStates.telefon)

async def get_phone(message: Message, state: FSMContext):
    user_data = await state.get_data()
    ism = user_data['ism']
    phone = message.contact.phone_number
    user_id = message.from_user.id

    # 👇 Shu yerda siz bazaga yozishingiz mumkin (masalan SQLAlchemy yoki SQLite)
    # save_user(user_id=user_id, name=ism, phone=phone)
    user_text = f"🆕 Yangi foydalanuvchi:\n\n👤 ID: {user_id}\n😀 Ism: {ism}\n📞 Telefon: {phone}"
    if search_user_by_id(user_id):
        await message.answer("Siz allaqachon ro'yxatdan o'tgansiz!", reply_markup=None)
        return
    else:
        add_user(ism=ism, telefon=phone, user_id=user_id)  # bazaga yozish
    await message.answer(f"✅ Ro'yxatdan o'tdingiz!\nIsm: {ism}\nTelefon: {phone}", reply_markup=None)
    for admin_id in ADMINS:
        await message.bot.send_message(admin_id, user_text)
    await message.answer("Ro'yxatdan o'tish tugallandi. Endi siz botdan foydalanishingiz mumkin!", reply_markup=None)
    await state.clear()


def register_start_handler(dp: Dispatcher):
    dp.message.register(start_registration, F.text == "👤 Ro'yhatdan o'tish")
    dp.message.register(get_name, RegisterStates.ism)
    dp.message.register(get_phone, RegisterStates.telefon, F.contact)
