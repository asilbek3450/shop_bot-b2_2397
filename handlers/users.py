from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import MenuStates
from database import add_category_to_db, get_category_id_by_name, add_product_to_db, get_product_id_by_name, get_product_by_id
from keyboards import tasdiqlash_keyboard, admin_keyboard, get_category_keyboard, get_product_keyboard, in_product_keyboard
from aiogram.types import ReplyKeyboardRemove


async def menu_handler(message: Message, state: FSMContext):
    await message.answer("Kerakli kategoriyani tanlang:", reply_markup=get_category_keyboard())
    await state.set_state(MenuStates.category_selection)

async def get_category_name(message: Message, state: FSMContext):
    kategory_name = message.text
    await state.update_data(category_name=kategory_name)
    try:
        kategory_id = get_category_id_by_name(kategory_name)
        await message.answer("📂 Kategoriyaga tegishli mahsulotni tanlang:", reply_markup=get_product_keyboard(category_id=kategory_id))
        await state.set_state(MenuStates.product_selection)
    except ValueError:
        await message.answer("❌ Bunday kategoriya mavjud emas. Iltimos, qayta urinib ko'ring.", reply_markup=get_category_keyboard())
    
    
async def get_product_name(message: Message, state: FSMContext):
    product_name = message.text
    try:
        product_id = get_product_id_by_name(product_name)
        product = get_product_by_id(product_id)
        image_caption = f"📦 Mahsulot: {product[1]}\n💰 Narx: {product[2]} $\n📄 Tavsif: {product[4]}"
        await message.answer_photo(photo=product[3], caption=image_caption, reply_markup=in_product_keyboard(product_id=product_id))
    except ValueError:
        await message.answer("❌ Bunday mahsulot mavjud emas. Iltimos, qayta urinib ko'ring.", reply_markup=get_product_keyboard(category_id=product[5]))
            

def register_menu_handlers(dp):
    dp.message.register(menu_handler, F.text == "📋 Menyu")
    dp.message.register(get_category_name, MenuStates.category_selection, F.text)
    dp.message.register(get_product_name, MenuStates.product_selection, F.text)