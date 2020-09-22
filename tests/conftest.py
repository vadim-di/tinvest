import pytest

from tinvest.schemas import Empty, Error


@pytest.fixture()
def token():
    return '<TOKEN>'


@pytest.fixture()
def figi():
    return 'BBG0013HGFT4'


@pytest.fixture()
def broker_account_id():
    return 'some_broker_account_id'


@pytest.fixture()
def error():
    return Error(
        trackingId='tracking_id',
        payload={},
    )


@pytest.fixture()
def empty():
    return Empty(
        trackingId='tracking_id',
        payload={},
    )
