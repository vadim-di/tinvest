# pylint:disable=redefined-outer-name
from datetime import datetime, timedelta

import pytest

from tinvest import OperationsApi, OperationsResponse


@pytest.fixture()
def api_client(http_client):
    return OperationsApi(http_client)


def test_operations_get(api_client, http_client, figi, broker_account_id):
    to = datetime.now()
    from_ = to - timedelta(days=7)
    api_client.operations_get(
        from_.isoformat(), to.isoformat(), figi, broker_account_id
    )
    http_client.request.assert_called_once_with(
        'GET',
        '/operations',
        response_model=OperationsResponse,
        params={
            'figi': figi,
            'brokerAccountId': broker_account_id,
            'from': from_.isoformat(),
            'to': to.isoformat(),
        },
    )


def test_operations_get_without_optional_args(api_client, http_client):
    to = datetime.now()
    from_ = to - timedelta(days=7)
    api_client.operations_get(from_.isoformat(), to.isoformat())
    http_client.request.assert_called_once_with(
        'GET',
        '/operations',
        response_model=OperationsResponse,
        params={'from': from_.isoformat(), 'to': to.isoformat()},
    )
