from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import CategoryStates, ProductStates
from database import add_category_to_db
from keyboards import tasdiqlash_keyboard, admin_keyboard


async def add_category(message: Message, state: FSMContext):
    await message.answer("📂 Iltimos, kategoriya nomini kiriting:")
    await state.set_state(CategoryStates.category_name)
    
async def get_category_name(message: Message, state: FSMContext):
    await state.update_data(category_name=message.text)
    await message.answer("📂 Kategoriya nomi qabul qilindi. Buni tasdiqlayizmi?", reply_markup=tasdiqlash_keyboard)
    await state.set_state(CategoryStates.tasdiqlash)
    
async def confirm_category(message: Message, state: FSMContext):
    user_data = await state.get_data()
    category_name = user_data['category_name']
    if message.text == "✅ Tasdiqlash":
        add_category_to_db(category_name)
        await message.answer(f"✅ Kategoriya qo'shildi: {category_name}", reply_markup=None)
    else:
        await message.answer("❌ Kategoriya qo'shish bekor qilindi.\n📂 Iltimos, kategoriya nomini boshqatdan kiriting:")
        await state.set_state(CategoryStates.category_name)
             
        
def register_category_handlers(dp):
    dp.message.register(add_category, F.text == "➕ Kategoriya qo‘shish")
    dp.message.register(get_category_name, CategoryStates.category_name)
    dp.message.register(confirm_category, CategoryStates.tasdiqlash, F.text.in_({"✅ Tasdiqlash", "❌ Bekor qilish"}))
    