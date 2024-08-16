from aiogram.utils.i18n import FSMI18nMiddleware, I18n
from pathlib import Path

WORKDIR = Path(__file__).parent.parent

i18n = FSMI18nMiddleware(I18n(path=WORKDIR / "locales", default_locale="ru", domain="messages"))
