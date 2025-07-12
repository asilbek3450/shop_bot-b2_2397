from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import CategoryStates, ProductStates
from database import add_category_to_db, get_category_id_by_name, add_product_to_db
from keyboards import tasdiqlash_keyboard, admin_keyboard, get_category_keyboard


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
        await message.answer("❌ Kategoriya qo'shish bekor qilindi.")
        await state.clear()
        await message.answer("Kerakli bo'limni tanlang:", reply_markup=admin_keyboard)
        
        
def register_category_handlers(dp):
    dp.message.register(add_category, F.text == "➕ Kategoriya qo‘shish")
    dp.message.register(get_category_name, CategoryStates.category_name)
    dp.message.register(confirm_category, CategoryStates.tasdiqlash, F.text.in_({"✅ Tasdiqlash", "❌ Bekor qilish"}))
    
    
    
async def add_product(message: Message, state: FSMContext):
    await message.answer("📂 Iltimos, product nomini kiriting:")
    await state.set_state(ProductStates.product_name)
    
async def get_product_name(message: Message, state: FSMContext):
    await state.update_data(product_name=message.text)
    await message.answer("📂 Product nomi qabul qilindi. Uni narxini kiriting:")
    await state.set_state(ProductStates.product_price)
    
    
async def get_product_price(message: Message, state: FSMContext):
    await state.update_data(product_price=message.text)
    await message.answer("📂 Product narxi qabul qilindi. Endi product rasmni yuboring:")
    await state.set_state(ProductStates.product_image)
    
    
async def get_product_image(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data(product_image=message.photo[-1].file_id)
        await message.answer("📂 Product rasm qabul qilindi. Endi product tavsifini kiriting:")
        await state.set_state(ProductStates.product_description)
    else:
        await message.answer("❌ Iltimos, rasm yuboring.")
        
async def get_product_description(message: Message, state: FSMContext):
    await state.update_data(product_description=message.text)
    await message.answer("📂 Product tavsifi qabul qilindi. Endi product kategoriyasini tanlang:", reply_markup=get_category_keyboard())
    await state.set_state(ProductStates.product_category)
    
    
async def get_product_category(message: Message, state: FSMContext):
    user_data = await state.get_data()
    product_name = user_data['product_name']
    product_price = user_data['product_price']
    product_image = user_data['product_image']
    product_description = user_data['product_description']
    category_name = message.text
    category_id = get_category_id_by_name(category_name)
    await state.update_data(product_category=category_id)
    
    user_caption = (
        f"🆕 Yangi mahsulot:\n\n"
        f"📦 Nom: {product_name}\n"
        f"💰 Narx: {product_price}\n"
        f"📝 Tavsif: {product_description}\n" 
        f"📂 Kategoriya: {category_name}\n"
    )
    await message.answer_photo(photo=product_image, caption=user_caption, reply_markup=tasdiqlash_keyboard)
    await state.set_state(ProductStates.tasdiqlash) 
    
    
async def confirm_product(message: Message, state: FSMContext):
    user_data = await state.get_data()
    product_name = user_data['product_name']
    product_price = user_data['product_price']
    product_image = user_data['product_image']
    product_description = user_data['product_description']
    category_id = user_data['product_category']
    
    if message.text == "✅ Tasdiqlash":
        add_product_to_db(nomi=product_name, narxi=product_price, rasmi=product_image, malumot=product_description, category_id=category_id)
        await message.answer(f"✅ Mahsulot qo'shildi: {product_name}", reply_markup=None)
    else:
        await message.answer("❌ Mahsulot qo'shish bekor qilindi.")
    
    await state.clear()
    await message.answer("Kerakli bo'limni tanlang:", reply_markup=admin_keyboard)
    
    
def register_product_handlers(dp):
    dp.message.register(add_product, F.text == "📦 Mahsulot qo‘shish")
    dp.message.register(get_product_name, ProductStates.product_name)
    dp.message.register(get_product_price, ProductStates.product_price)
    dp.message.register(get_product_image, ProductStates.product_image)
    dp.message.register(get_product_description, ProductStates.product_description)
    dp.message.register(get_product_category, ProductStates.product_category)
    dp.message.register(confirm_product, ProductStates.tasdiqlash, F.text.in_({"✅ Tasdiqlash", "❌ Bekor qilish"}))
    
    