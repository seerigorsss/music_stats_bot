from aiogram.utils.i18n import FSMI18nMiddleware, I18n

i18n = FSMI18nMiddleware(I18n(path="app/locales", default_locale="ru", domain="messages"))
