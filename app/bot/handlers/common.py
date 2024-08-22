import datetime as dt
import logging

from aiogram import Router, filters, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.deep_linking import create_start_link, decode_payload

from bot.FSM.switch_to_fsm import go_to_fsm
from bot.utils.texts import _
from db.methods.user import create_or_update_user

# Logging common.py
logger = logging.getLogger(__name__)
router = Router()


# Handling /start with or without deep links
@router.message(Command(commands=['start']))
async def cmd_start(message: types.Message, state: FSMContext, command: filters.CommandObject, bot: Bot):
    raw_data = message.from_user
    user_id = raw_data.id
    username = raw_data.username
    status = None
    referer_login = None
    language_code = raw_data.language_code
    registration_date = dt.datetime.now(dt.timezone.utc)
    last_active = dt.datetime.now(dt.timezone.utc)
    args = command.args
    await go_to_fsm(state)
    if args:
        try:
            user_login = decode_payload(args)
            referer_login = user_login
            await state.update_data(user_login=user_login)
            await message.answer(_('START_FROM_FRIEND_MESSAGE')(user_login=user_login))

            await create_or_update_user(user_id=user_id, status=status, username=username, referer_login=referer_login,
                              language_code=language_code, registration_date=registration_date,
                              last_active=last_active)
        except:
            logger.error(f'Error in start link: {args}')
            await message.answer(_('BAD_LINK_MESSAGE')())
            await state.clear()
    else:
        await message.answer(_('START_MESSAGE')())
        await create_or_update_user(user_id=user_id, status=status, username=username, referer_login=referer_login,
                          language_code=language_code, registration_date=registration_date,
                          last_active=last_active)
