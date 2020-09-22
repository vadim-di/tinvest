# pylint:disable=redefined-outer-name
import asynctest
import pytest

from tinvest.async_client import AsyncClient, ClientSession
from tinvest.constants import PRODUCTION
from tinvest.schemas import Empty


@pytest.fixture()
async def session(mocker):
    _session = ClientSession()
    mocker.patch.object(
        _session,
        'request',
        return_value=asynctest.MagicMock(autospec=True),
        autospec=True,
    )
    yield _session
    await _session.close()


@pytest.fixture()
def client(token, session):
    return AsyncClient(
        token,
        session=session,
    )


@pytest.mark.asyncio
async def test_client_request(client, session, token):
    async with client.request('get', '/some_url', response_model=Empty):
        pass
    session.request.assert_called_once_with(
        'get',
        f'{PRODUCTION}/some_url',
        headers={'Authorization': f'Bearer {token}', 'accept': 'application/json'},
    )


@pytest.mark.asyncio
async def test_client_response(client):
    async with client.request('get', '/some_url', response_model=Empty) as response:
        assert 'parse_json' in dir(response)
        assert 'parse_error' in dir(response)


@pytest.mark.asyncio
async def test_client_session_close(client):
    await client.close()
