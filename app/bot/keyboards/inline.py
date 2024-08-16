from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.utils.texts import _


def make_result_keyboard(link):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=_('SHARE_RESULT_MESSAGE')(),
        url=link)
    )
    return builder.as_markup()
