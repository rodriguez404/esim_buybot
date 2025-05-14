# Заглушка, если подключение к Redis не удалось - должен логировать ошибки
class AsyncDummyRedis:
    async def get(self, *args, **kwargs):
        return None

    async def set(self, *args, **kwargs):
        return False

    async def ping(self):
        return False

    def __getattr__(self, name):
        async def method(*args, **kwargs):
            print(f"Redis недоступен: попытка вызвать {name}")
            return None
        return method