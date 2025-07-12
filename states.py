from aiogram.fsm.state import StatesGroup, State

class RegisterStates(StatesGroup):
    ism = State()
    telefon = State()

class CategoryStates(StatesGroup):
    category_name = State()
    tasdiqlash = State()
    

class ProductStates(StatesGroup):
    product_name = State()
    product_price = State()
    product_image = State()
    product_description = State()
    product_category = State()
    tasdiqlash = State()
    
    
class MenuStates(StatesGroup):
    category_selection = State()
    product_selection = State()
    
    