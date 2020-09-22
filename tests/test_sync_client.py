# pylint:disable=redefined-outer-name
import pytest

from tinvest.constants import PRODUCTION
from tinvest.schemas import Empty
from tinvest.sync_client import ResponseWrapper, Session, SyncClient


@pytest.fixture()
def session(mocker):
    _session = Session()
    mocker.patch.object(_session, 'request', autospec=True)
    return _session


@pytest.fixture()
def client(token, session):
    return SyncClient(
        token,
        session=session,
    )


def test_client_request(client, session, token):
    client.request('get', '/some_url', response_model=Empty)
    session.request.assert_called_once_with(
        method='get',
        url=f'{PRODUCTION}/some_url',
        headers={'Authorization': f'Bearer {token}', 'accept': 'application/json'},
    )


def test_client_response(client):
    response = client.request('get', '/some_url', response_model=Empty)
    assert isinstance(response, ResponseWrapper)


def test_client_response_with_raise_for_status(client):
    response = client.request(
        'get', '/some_url', response_model=Empty, raise_for_status=True
    )
    response.raise_for_status.assert_called_once_with()


def test_client_response_with_session(token):
    client = SyncClient(token)
    assert isinstance(client.session, Session)


def test_response_wrapper_error(mocker, error):
    response = mocker.Mock()
    response.json.return_value = error.dict(by_alias=True)
    response_wrapper = ResponseWrapper(response, Empty)

    assert response_wrapper.parse_error() == error


def test_response_wrapper_empty(mocker, empty):
    response = mocker.Mock()
    response.json.return_value = empty.dict(by_alias=True)
    response_wrapper = ResponseWrapper(response, Empty)

    assert response_wrapper.parse_json() == empty


def test_response_wrapper_attr(mocker):
    response = mocker.Mock()
    response.json.return_value = {}
    response_wrapper = ResponseWrapper(response, Empty)

    assert response_wrapper.json() == {}
