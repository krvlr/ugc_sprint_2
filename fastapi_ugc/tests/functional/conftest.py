import json

import pytest_asyncio
import aiohttp

from .settings import test_settings
from .utils.jwt_creator import get_jwt_token

pytest_plugins = ["fixtures.mongo_fixtures",]


@pytest_asyncio.fixture(scope='function')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture
def get_token_header():
    async def inner() -> dict:
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": "Bearer " + get_jwt_token(),
        }
        return headers

    return inner


@pytest_asyncio.fixture
def make_get_request(session: aiohttp.ClientSession):
    async def inner(endpoint: str,
                    headers={},
                    query_data: dict = {}) -> dict:
        url = f"{test_settings.service_url}{endpoint}"
        print(url)
        response = await session.get(url=url,
                                     headers=headers,
                                     params=query_data)
        try:
            resp_json = await response.json()
        except:
            resp_json = str(response)
        return {
            'body': resp_json,
            'status': response.status,
        }

    return inner


@pytest_asyncio.fixture
def make_post_request(session: aiohttp.ClientSession):
    async def inner(endpoint: str,
                    headers={},
                    data={}) -> dict:
        url = f"{test_settings.service_url}{endpoint}"
        response = await session.post(url=url,
                                      headers=headers,
                                      data=json.dumps(data))
        try:
            resp_json = await response.json()
        except:
            resp_json = str(response)
        return {
            'body': resp_json,
            'status': response.status,
        }

    return inner


@pytest_asyncio.fixture
def make_patch_request(session: aiohttp.ClientSession):
    async def inner(endpoint: str,
                    headers={},
                    data={}) -> dict:
        url = f"{test_settings.service_url}{endpoint}"
        response = await session.patch(url=url,
                                       headers=headers,
                                       data=json.dumps(data))
        try:
            resp_json = await response.json()
        except:
            resp_json = str(response)
        return {
            'body': resp_json,
            'status': response.status,
        }

    return inner


@pytest_asyncio.fixture
def make_put_request(session: aiohttp.ClientSession):
    async def inner(endpoint: str,
                    headers={},
                    data={}) -> dict:
        url = f"{test_settings.service_url}{endpoint}"
        response = await session.put(url=url,
                                     headers=headers,
                                     data=json.dumps(data))
        try:
            resp_json = await response.json()
        except:
            resp_json = str(response)
        return {
            'body': resp_json,
            'status': response.status,
        }

    return inner


@pytest_asyncio.fixture
def make_delete_request(session: aiohttp.ClientSession):
    async def inner(endpoint: str,
                    headers={},
                    data={}) -> dict:
        url = f"{test_settings.service_url}{endpoint}"
        response = await session.delete(url=url,
                                        headers=headers,
                                        data=json.dumps(data))
        try:
            resp_json = await response.json()
        except:
            resp_json = str(response)
        return {
            'body': resp_json,
            'status': response.status,
        }

    return inner