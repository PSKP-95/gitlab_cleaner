

import asyncio
from random import randint

import aiohttp

session = None

def init_session():
    global session
    session = aiohttp.ClientSession()

async def close_session():
    global session
    await session.close()

async def task(url, headers, method, data, context):
    global calls, http_codes, session

    if session == None:
        init_session()
    
    await asyncio.sleep(randint(0, 20))
    response = await session.request(method, url, headers = headers, data=data)
    
    context["project"].calls[response.status] = (context.get("project").calls.get(response.status) or 0) + 1
    return (response, context)

async def json_task(response: aiohttp.ClientResponse, context):
    jsonResponse = await response.json()
    return (jsonResponse, context)