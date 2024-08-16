from aiogram.utils.i18n import gettext


def _(text: str):
    def getargstranslation(**kwargs):
        return gettext(text).format(**kwargs)

    return getargstranslation
