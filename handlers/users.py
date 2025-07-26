from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import MenuStates, ZakazStates
from database import get_all_categories, get_all_products

from database import add_category_to_db, get_category_id_by_name, add_product_to_db, get_product_id_by_name, get_product_by_id
import database
from keyboards import tasdiqlash_keyboard, admin_keyboard, get_category_keyboard, get_product_keyboard, in_product_keyboard, user_keyboard
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
        await state.clear()
    except ValueError:
        await message.answer("❌ Bunday mahsulot mavjud emas. Iltimos, qayta urinib ko'ring.", reply_markup=get_product_keyboard(category_id=product[5])) # type: ignore
            
            
async def add_to_cart(callback_query, state: FSMContext):
    product_id = int(callback_query.data.split("_")[-1])
    user_id = callback_query.from_user.id  # type: ignore
    
    # Foydalanuvchi savatiga mahsulot qo'shish
    database.add_zakaz(user_id=user_id, product_id=product_id, soni=1)  # Soni 1 deb belgilaymiz
    await callback_query.message.answer("✅ Mahsulot savatga qo'shildi!", reply_markup=user_keyboard)
    
    await state.clear()  # Holatni tozalash
    

async def zakaz_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id  # type: ignore
    zakazlar = database.get_zakazlar_by_user_id(user_id)  # Foydalanuvchi bo'yicha barcha zakazlarni olish
    if not zakazlar:
        await message.answer("Sizda hech qanday zakaz mavjud emas.", reply_markup=user_keyboard)
        return
    
    zakaz_text = "Sizning zakazlaringiz:\n\n"
    print(zakazlar)
    for zakaz in zakazlar:
        print(zakaz)
        product = database.get_product_by_id(zakaz[0])  # Zakazdagi mahsulot ma'lumotlarini olish
        print(product, zakaz)
        zakaz_text += f"📦 Mahsulot: {product[1]}, \n🔢 Soni: {zakaz[2]}, \n💰 Narxi: {product[2]} $\n\n"
    
    await message.answer(zakaz_text, reply_markup=tasdiqlash_keyboard)
    await state.set_state(ZakazStates.tasdiqlash)
    

async def zakaz_tasdiqlash(message: Message, state: FSMContext):
    if message.text == "✅ Tasdiqlash":
        user_id = message.from_user.id  # type: ignore
        zakazlar = database.get_zakazlar_by_user_id(user_id)
        if zakazlar:
            await message.answer("Sizning zakazingiz tasdiqlandi!\nUshbu karta raqamga to'lov qilib chek yuboring!\n\n9860600401238685", reply_markup=ReplyKeyboardRemove())
            database.delete_zakaz_by_id(user_id=user_id)  # Foydalanuvchi bo'yicha barcha zakazlarni o'chirish
        else:
            await message.answer("Sizda hech qanday zakaz mavjud emas.", reply_markup=user_keyboard)
    else:
        await message.answer("Zakaz bekor qilindi.", reply_markup=user_keyboard)
    
    await state.clear()
    


def register_menu_handlers(dp):
    dp.message.register(menu_handler, F.text == "📋 Menyu")
    dp.message.register(get_category_name, MenuStates.category_selection, F.text)
    dp.message.register(get_product_name, MenuStates.product_selection, F.text)
    dp.callback_query.register(add_to_cart, F.data.startswith("add_to_cart_"))
    dp.message.register(zakaz_handler, F.text == "🛒 Mening zakazlarim")
    dp.message.register(zakaz_tasdiqlash, ZakazStates.tasdiqlash, F.text)
    dp.message.register(lambda message: message.answer("Iltimos, menyudan tanlov qiling."), F.text)  # Default handler for unexpected messages
    
