from tortoise import Tortoise
from .config import DB_CONFIG

async def init_db():
    await Tortoise.init(config=DB_CONFIG)
    await Tortoise.generate_schemas()