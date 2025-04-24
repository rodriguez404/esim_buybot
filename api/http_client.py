import aiohttp

session: aiohttp.ClientSession | None = None

async def get_session() -> aiohttp.ClientSession:
    global session
    if session is None or session.closed:
        connector = aiohttp.TCPConnector(ttl_dns_cache=300)
        session = aiohttp.ClientSession(connector=connector)
    return session

async def close_session():
    global session
    if session and not session.closed:
        await session.close()
