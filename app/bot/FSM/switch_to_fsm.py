from aiogram.fsm.context import FSMContext
from bot.FSM.fsm_test import TestPolling


async def go_to_fsm(state: FSMContext):
    await state.set_state(TestPolling.sending_login)
