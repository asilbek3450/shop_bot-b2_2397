from aiogram.fsm.state import StatesGroup, State

class RegisterStates(StatesGroup):
    ism = State()
    telefon = State()

