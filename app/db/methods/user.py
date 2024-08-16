from db.models import User


async def create_or_update_user(user_id, status, username, referer_login, language_code, registration_date,
                                last_active):
    exists = await User.filter(user_id=user_id).exists()
    if not exists:
        await User.create(user_id=user_id, status=status, username=username,
                          referer_login=referer_login, language_code=language_code,
                          registration_date=registration_date, last_active=last_active)
    else:
        await User.filter(user_id=user_id).update(last_active=last_active)
