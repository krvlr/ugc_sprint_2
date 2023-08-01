import http
import uuid

import pytest


@pytest.mark.asyncio
async def test_get_bookmarks_list(make_get_request,
                                  get_token_header
):
    """Получение списка всех закладок."""
    token_header = await get_token_header()
    response = await make_get_request(f'/bookmarks/',
                                      token_header,
                                      {})
    # assert len(response['body']) == 0
    assert response['status'] == http.HTTPStatus.OK


@pytest.mark.asyncio
async def test_create_bookmark(make_post_request,
    get_token_header):
    """Проверка создания закладки."""
    token_header = await get_token_header()
    bookmark_data = {
        'film_id': str(uuid.uuid4())
    }
    response = await make_post_request(f'/bookmarks/create',
                                       token_header,
                                       bookmark_data)

    assert response['status'] == http.HTTPStatus.OK


@pytest.mark.asyncio
async def test_delete_bookmark(make_delete_request,
                               make_get_request,
                               make_post_request,
                               get_token_header,
):
    """Удаление закладки и проверка что ее после этого не существует."""

    token_header = await get_token_header()
    bookmark_data = {
        'film_id': str(uuid.uuid4())
    }
    film_uuid = bookmark_data['film_id']
    response = await make_post_request(f'/bookmarks/create',
                                       token_header,
                                       bookmark_data)

    assert response['status'] == http.HTTPStatus.OK

    response_delete = await make_get_request(f'/bookmarks/delete?film_id={film_uuid}',
                                             token_header,
                                             {})

    assert response_delete['status'] == http.HTTPStatus.OK
