from aiogram import types


def main_menu_keyboard():
    buttons = ['New message']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*buttons)
    return keyboard


def admin_orders(appeal_id: int):
    button = [
        types.InlineKeyboardButton(text="Відповісти",
                                   callback_data=f"adminconfirm, {appeal_id}"),
        types.InlineKeyboardButton(text="Відхилити", callback_data=f"admindelete, {appeal_id}")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*button)
    return keyboard


def hide_bag_buttons():
    buttons = [
        types.InlineKeyboardButton(text="👌",
                                   callback_data="pass")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard
