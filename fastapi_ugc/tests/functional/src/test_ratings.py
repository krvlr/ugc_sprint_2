import http
import uuid

import pytest


@pytest.mark.asyncio
async def test_get_ratings_list(make_get_request,
                                get_token_header):
    """Получение списка всех оценок."""
    token_header = await get_token_header()
    response = await make_get_request('/ratings/',
                                      token_header,
                                      {})
    # assert len(response['body']) == 1
    assert response['status'] == http.HTTPStatus.OK


@pytest.mark.asyncio
async def test_get_avg(make_get_request,
                       make_post_request,
                       get_token_header):
    """Получение средней оценки."""
    token_header = await get_token_header()
    rating_data = {
        'film_id': str(uuid.uuid4()),
        'rating_score': 10
    }
    film_uuid = rating_data['film_id']
    response = await make_post_request('/ratings/create',
                                       token_header,
                                       rating_data)
    assert response['status'] == http.HTTPStatus.OK

    response = await make_get_request(f'/ratings/avg/{film_uuid}',
                                      token_header,
                                      {})

    assert len(response['body']) == 2
    assert response['status'] == http.HTTPStatus.OK


@pytest.mark.asyncio
async def test_get_count(make_get_request,
                         make_post_request,
                         get_token_header):
    """Получение количества оценок."""
    token_header = await get_token_header()
    rating_data = {
        'film_id': str(uuid.uuid4()),
        'rating_score': 10
    }
    film_uuid = rating_data['film_id']
    response = await make_post_request('/ratings/create',
                                       token_header,
                                       rating_data)
    assert response['status'] == http.HTTPStatus.OK

    response = await make_get_request(f'/ratings/count/{film_uuid}',
                                      token_header,
                                      {})

    assert len(response['body']) == 2
    assert response['status'] == http.HTTPStatus.OK


@pytest.mark.asyncio
async def test_create_ratings(make_post_request,
                              get_token_header):
    """Проверка создания оценки."""
    token_header = await get_token_header()
    rating_data = {
        'film_id': str(uuid.uuid4()),
        'rating_score': 10
    }
    response = await make_post_request('/ratings/create',
                                       token_header,
                                       rating_data)

    assert response['status'] == http.HTTPStatus.OK


@pytest.mark.asyncio
async def test_update_ratings(make_post_request,
                              make_put_request,
                              get_token_header):
    """Проверка обновления оценки."""
    token_header = await get_token_header()
    rating_data = {
        'film_id': str(uuid.uuid4()),
        'rating_score': 10
    }
    response = await make_post_request('/ratings/create',
                                       token_header,
                                       rating_data)

    assert response['status'] == http.HTTPStatus.OK

    response = await make_put_request('/ratings/update',
                                      token_header,
                                      rating_data)

    assert response['status'] == http.HTTPStatus.OK


@pytest.mark.asyncio
async def test_delete_ratings(make_delete_request,
                              make_post_request,
                              get_token_header):
    """Удаление оценки и проверка что ее после этого не существует."""

    token_header = await get_token_header()
    rating_data = {
        'film_id': str(uuid.uuid4()),
        'rating_score': 10
    }
    film_uuid = rating_data['film_id']
    response = await make_post_request('/ratings/create',
                                       token_header,
                                       rating_data)
    assert response['status'] == http.HTTPStatus.OK

    response_delete = await make_delete_request(f'/ratings/delete?film_id={film_uuid}',
                                                token_header,
                                                {})
    assert response_delete['status'] == http.HTTPStatus.OK
