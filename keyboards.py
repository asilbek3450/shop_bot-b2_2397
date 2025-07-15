from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from database import get_all_categories, get_all_products
# 👑 Admin uchun keyboard
admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Kategoriya qo‘shish"), KeyboardButton(text="📦 Mahsulot qo‘shish")],
        [KeyboardButton(text="📋 Menyu"), KeyboardButton(text="⚙️ Sozlamalar")]
    ],
    resize_keyboard=True
)

# 👤 Oddiy foydalanuvchi uchun keyboard
user_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Menyu"), KeyboardButton(text="📞 Admin bilan bog‘lanish")],
        [KeyboardButton(text="⚙️ Sozlamalar"), KeyboardButton(text="🛒 Mening zakazlarim")],
        [KeyboardButton(text="📍 Manzil")]
    ],
    resize_keyboard=True
)
user_zakaz_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💰 Sotib olish"), KeyboardButton(text="❌ Bekor qilish")],
        [KeyboardButton(text="🔙 Orqaga")],
    ],
    resize_keyboard=True,
)

phone_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

register_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👤 Ro'yhatdan o'tish")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

tasdiqlash_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Tasdiqlash"), KeyboardButton(text="❌ Bekor qilish")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


def get_category_keyboard():
    categories = get_all_categories()
    buttons = [KeyboardButton(text=category[1]) for category in categories]
    keyboards = ReplyKeyboardMarkup(
        keyboard=[buttons[i:i + 2] for i in range(0, len(buttons), 2)],
        resize_keyboard=True
    )
    return keyboards


def get_product_keyboard(category_id):
    products = get_all_products(category_id)
    buttons = [KeyboardButton(text=product[1]) for product in products]
    keyboards = ReplyKeyboardMarkup(
        keyboard=[buttons[i:i + 2] for i in range(0, len(buttons), 2)],
        resize_keyboard=True
    )
    return keyboards


def in_product_keyboard(product_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="-", callback_data=f"decrease_quantity_{product_id}"),
                InlineKeyboardButton(text="🛒 Savatga qo'shish", callback_data=f"add_to_cart_{product_id}"),
                InlineKeyboardButton(text="+", callback_data=f"increase_quantity_{product_id}")
            ],
            [
                InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_products")
            ]
        ], resize_keyboard=True
    )
    
            