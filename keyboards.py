from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
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
