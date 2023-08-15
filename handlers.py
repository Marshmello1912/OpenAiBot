from aiogram import Dispatcher, types
from Gen import create_text_answer, create_image_answer
from aiogram.dispatcher import FSMContext
from States import Form
import keyboard


async def start_command(message: types.Message, state: FSMContext):
    await message.answer("Бот готов к работе!", reply_markup= keyboard.selectChat)


async def help_command(message: types.Message, state: FSMContext):
    await message.answer(
        """Данный бот предназначен для более легкого обращения к сервисам OpenAi, в частности:Chat-GPT3 и DALL-E.
Чтобы обратиться с вопросом к Chat-Gpt испольуйте комманду /ask запрос
Пример:
/ask Напиши сортировку пузырьком на Python.
    
Чтобы оратиться с запросом к DALL-E используйте команду /img запрос
Пример:
/img Зеленый кот.""")


async def gpt_set(callback_query: types.CallbackQuery, state: FSMContext):
    await Form.Gpt.set()
    await callback_query.message.delete()
    await callback_query.message.answer("Ожидаю запрос...", reply_markup=keyboard.exitChat)


async def get_gpt_answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data._data == {}:
            data['questions'] = [
                {"role": 'system', "content": "You are a helpful assistant."},
                {"role": 'user', "content": message.text}]
            answer = await create_text_answer(data['questions'])
            data['questions'].append({"role": 'assistant', "content": answer})
        else:
            data['questions'].append({"role": 'user', "content": message.text})
            answer = await create_text_answer(data["questions"])
            data['questions'].append({"role": 'assistant', "content": answer})
    await message.answer(answer)


async def dalle_set(callback_query: types.callback_query, state: FSMContext):
    await Form.Dalle.set()
    await callback_query.message.delete()
    await callback_query.message.answer('Теперь укажите промпт...', reply_markup=keyboard.exitChat)


async def get_dalle_answer(message: types.Message, state: FSMContext):
    answer = await create_image_answer(message.text)
    imgs = []
    for i in answer:
        imgs.append(types.input_media.InputMediaPhoto(i.url))

    await message.answer_media_group(imgs)


async def exit_from_states(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Вы вышли из состояния запроса', reply_markup=keyboard.clear)
    await start_command(message,state)
    await message.delete()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(exit_from_states, lambda m:m.text == 'На главную', state='*')
    dp.register_callback_query_handler(gpt_set,lambda c:c.data =='/ask', state=None)
    dp.register_message_handler(get_gpt_answer, state=Form.Gpt)
    dp.register_callback_query_handler(dalle_set, lambda c:c.data == '/img', state=None)
    dp.register_message_handler(get_dalle_answer, state=Form.Dalle)
    dp.register_message_handler(help_command, commands=['help'])
