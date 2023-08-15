from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    Gpt = State()
    Dalle = State()
