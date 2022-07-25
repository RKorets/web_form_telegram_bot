import logging
import asyncio

from aiogram import executor, types, Dispatcher, Bot
from aiogram.dispatcher.filters import Text
import aiogram.utils.markdown as md
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from models import WebUserForm
from sqlalchemy import select
from db import session

import keyboard
from sender import send_email

storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot('YOU_API_TOKEN')

dp = Dispatcher(bot=bot, storage=storage)
admin_list = [368553201]


class Form(StatesGroup):
    tech_answer = State()


def auth(func):
    async def wrapper(message):
        if isinstance(message, types.CallbackQuery):
            if message.message.chat.id not in admin_list:
                return await message.answer(f'Я не зрозумів твою команду')
            return await func(message)
        elif isinstance(message, types.Message):
            if message.chat.id not in admin_list:
                return await message.answer(f'Я не зрозумів твою команду')
            return await func(message)
        return await message.answer(f'Я не зрозумів твою команду')

    return wrapper


@dp.message_handler(commands=['start'])
@auth
async def start(message: types.message):
    caption = f'Привіт {message.from_user.first_name}, я message-Bot '
    print(message.from_user)

    await bot.send_message(message.chat.id, caption, reply_markup=keyboard.main_menu_keyboard())


@dp.message_handler(Text(startswith=['New message']))
@auth
async def admin_support(message: types.Message):
    message_queries = select(WebUserForm).filter(WebUserForm.status == 'new')
    new_message = session.execute(message_queries).scalars()
    new_orders = new_message.fetchall()
    session.close()
    if len(new_orders):
        for m in new_orders:
            answer = []
            answer.append(f'id: {m.id}')
            answer.append(f'Username: {m.username}')
            answer.append(f'Email: {m.email}')
            answer.append(f'Appeal: {m.type_appeal}')
            answer.append(f'Message: {m.message}')
            await message.answer('\n'.join(answer), reply_markup=keyboard.admin_orders(m.id))
    else:
        await message.answer('Empty')


answer_user_data = []
loop = asyncio.get_event_loop()
DELAY = {'time_delay': 60.0}


@dp.callback_query_handler(Text(startswith=["adminconfirm", "admindelete"]))
async def admin_order_status(call: types.CallbackQuery):
    answer = call.data.split(',')
    appeal_id = int(answer[1])
    if call.data.startswith("adminconfirm"):
        user = session.query(WebUserForm).filter(WebUserForm.id == appeal_id).first()
        answer_user_data.append((appeal_id, user.email))
        session.close()
        await bot.send_message(call.message.chat.id, f'Send answer for {appeal_id}:')
        await Form.tech_answer.set()
    else:
        session.query(WebUserForm).filter(WebUserForm.id == appeal_id).update({WebUserForm.status: 'cancel'})
        session.commit()
        session.close()
    await call.message.edit_reply_markup(reply_markup=keyboard.hide_bag_buttons())
    await call.answer()


@dp.message_handler(state=Form.tech_answer)
async def tech_answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tech_answer'] = message.text
        appeal_id, user_email = answer_user_data[0]
        send = send_email(md.text(data['tech_answer']), user_email)
        if send:
            session.query(WebUserForm).filter(WebUserForm.id == appeal_id).update({WebUserForm.status: 'send'})
            session.commit()
            session.close()
            answer_user_data.clear()
            DELAY['time_delay'] = 60.0
            await bot.send_message(message.chat.id, 'Success send')
        else:
            answer_user_data.clear()
            DELAY['time_delay'] = 60.0
            await bot.send_message(message.chat.id, 'Error send, try again')
    await state.finish()


async def check_new_message():
    message_queries = select(WebUserForm).filter(WebUserForm.status == 'new')
    new_message = session.execute(message_queries).scalars()
    new_orders = new_message.fetchall()
    session.close()
    if len(new_orders):
        DELAY['time_delay'] = 600.0
        await bot.send_message(admin_list[0], 'New message from web')
    when_to_call = loop.time() + DELAY['time_delay']
    loop.call_at(when_to_call, start_callback)


def start_callback():
    asyncio.ensure_future(check_new_message())


if __name__ == "__main__":
    start_callback()
    executor.start_polling(dp)
    loop.run_forever()