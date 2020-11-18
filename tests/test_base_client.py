# pylint:disable=redefined-outer-name
import pytest

from tinvest.base_client import BaseClient
from tinvest.constants import PRODUCTION, SANDBOX


class Client(BaseClient):
    def request(self, *args, **kwargs):
        pass


def test_create_client(token):
    session = object()
    client = Client(token, session=session)

    assert client._base_url == PRODUCTION  # pylint:disable=protected-access
    assert client.session is session


def test_create_client_with_empty_token():
    with pytest.raises(ValueError, match='^Token can not be empty$'):
        Client('')


def test_create_client_for_sandbox(token):
    client = Client(token, use_sandbox=True)

    assert client._base_url == SANDBOX  # pylint:disable=protected-access


def test_create_client_without_session(token):
    client = Client(token)
    with pytest.raises(AttributeError):
        assert not client.session
