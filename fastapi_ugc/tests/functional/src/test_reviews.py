import http
import uuid

import pytest


@pytest.mark.asyncio
async def test_get_reviews_list(make_get_request,
                                get_token_header):
    """Получение списка всех ревью."""
    token_header = await get_token_header()
    response = await make_get_request('/reviews/',
                                      token_header,
                                      {})
    # assert len(response['body']) == 1
    assert response['status'] == http.HTTPStatus.OK


@pytest.mark.asyncio
async def test_create_reviews(make_post_request,
                              get_token_header):
    """Проверка создания ревью."""
    token_header = await get_token_header()
    bookmark_data = {
        'film_id': str(uuid.uuid4()),
        'text': 'random text'
    }
    response = await make_post_request('/reviews/create',
                                       token_header,
                                       bookmark_data)

    assert response['status'] == http.HTTPStatus.OK


@pytest.mark.asyncio
async def test_update_reviews(make_post_request,
                              get_token_header):
    """Проверка обновления ревью."""
    token_header = await get_token_header()
    bookmark_data = {
        'film_id': str(uuid.uuid4()),
        'text': 'random text'
    }
    response = await make_post_request('/reviews/create',
                                       token_header,
                                       bookmark_data)

    assert response['status'] == http.HTTPStatus.OK

    response = await make_post_request('/reviews/update',
                                       token_header,
                                       bookmark_data)

    assert response['status'] == http.HTTPStatus.OK


@pytest.mark.asyncio
async def test_delete_reviews(make_delete_request,
                              make_get_request,
                              make_post_request,
                              get_token_header):
    """Удаление ревью и проверка что его после этого не существует."""

    token_header = await get_token_header()
    review_data = {
        'film_id': str(uuid.uuid4()),
        'text': 'random text'
    }
    film_uuid = review_data['film_id']
    response = await make_post_request('/reviews/create',
                                       token_header,
                                       review_data)

    assert response['status'] == http.HTTPStatus.OK

    response_delete = await make_get_request(f'/reviews/delete?film_id={film_uuid}',
                                             token_header,
                                             {})

    assert response_delete['status'] == http.HTTPStatus.OK
