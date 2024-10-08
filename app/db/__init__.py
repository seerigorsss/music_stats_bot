from configs.settings import env_parameters
from tortoise import Tortoise

db_url = 'postgres://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


async def init():
    await Tortoise.init(
        db_url=db_url.format(DB_USERNAME=env_parameters.DB_USERNAME,
                             DB_PASSWORD=env_parameters.DB_PASSWORD,
                             DB_HOST=env_parameters.DB_HOST,
                             DB_PORT=env_parameters.DB_PORT,
                             DB_NAME=env_parameters.DB_NAME),
        modules={'models': ['db.models']})
    await Tortoise.generate_schemas()
