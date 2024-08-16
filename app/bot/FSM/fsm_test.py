import logging
import datetime as dt

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.deep_linking import create_start_link

import main
import music.test
from bot.keyboards import inline
from bot.utils.texts import _
from db.methods.user import create_or_update_user

# Logging test_polling.py
logger = logging.getLogger(__name__)

router = Router()


class TestPolling(StatesGroup):
    sending_login = State()
    send_results = State()


@router.message(TestPolling.sending_login)
async def send_login(message: types.Message, state: FSMContext):
    value = await music.test.get_songs_list(message.text)
    user_data = await state.get_data()
    raw_data = message.from_user
    user_id = raw_data.id
    username = raw_data.username
    status = None
    referer_login = None
    language_code = raw_data.language_code
    registration_date = dt.datetime.now(dt.timezone.utc)
    last_active = dt.datetime.now(dt.timezone.utc)
    if value:
        await message.answer(_('SENDING_LOGIN_MESSAGE')())
        artist_dict = value['artists']
        album_dict = value['albums']
        genre_dict = value['genres']
        track_count = value['track_count']
        owner = value['owner']
        link = await deep_link(owner)
        answer = await music.test.get_stats(artist_dict, album_dict, genre_dict, track_count, owner)
        await message.answer_photo(
            'https://music.yandex.ru/blocks/playlist-cover/playlist-cover_like.png',
            caption=answer, reply_markup=inline.make_result_keyboard(link)
        )
        if 'user_login' in user_data.keys():
            user_login = user_data['user_login']
            answer = await music.test.get_common_stats(owner, user_login)
            await message.answer(answer, reply_markup=inline.make_result_keyboard(link))
        await state.clear()
    else:
        await message.answer(_('INVALID_LOGIN_MESSAGE')())
    # await create_or_update_user(user_id=user_id, status=status, username=username, referer_login=referer_login,
    #                             language_code=language_code, registration_date=registration_date,
    #                             last_active=last_active)


async def deep_link(user_login):
    link = await create_start_link(main.bot, payload=user_login, encode=True)
    return link
