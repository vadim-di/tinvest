# pylint:disable=redefined-outer-name
import pytest

from tinvest import (
    BrokerAccountType,
    Empty,
    SandboxApi,
    SandboxRegisterRequest,
    SandboxRegisterResponse,
    SandboxSetCurrencyBalanceRequest,
    SandboxSetPositionBalanceRequest,
)


@pytest.fixture()
def api_client(http_client):
    return SandboxApi(http_client)


def test_sandbox_register(api_client, http_client):
    body = SandboxRegisterRequest(broker_account_type=BrokerAccountType.tinkoff)
    api_client.sandbox_register_post(body)
    http_client.request.assert_called_once_with(
        'POST',
        '/sandbox/register',
        response_model=SandboxRegisterResponse,
        data=body.json(by_alias=True),
    )


def test_sandbox_currencies_balance(api_client, http_client, broker_account_id):
    body = SandboxSetCurrencyBalanceRequest.parse_obj(
        {'balance': 1000.0, 'currency': 'USD'}
    )
    api_client.sandbox_currencies_balance_post(body, broker_account_id)
    http_client.request.assert_called_once_with(
        'POST',
        '/sandbox/currencies/balance',
        response_model=Empty,
        params={'brokerAccountId': broker_account_id},
        data=body.json(by_alias=True),
    )


def test_sandbox_currencies_balance_without_broker_account_id(api_client, http_client):
    body = SandboxSetCurrencyBalanceRequest.parse_obj(
        {'balance': 1000.0, 'currency': 'USD'}
    )
    api_client.sandbox_currencies_balance_post(body)
    http_client.request.assert_called_once_with(
        'POST',
        '/sandbox/currencies/balance',
        response_model=Empty,
        params={},
        data=body.json(by_alias=True),
    )


def test_sandbox_positions_balance(api_client, http_client, broker_account_id):
    body = SandboxSetPositionBalanceRequest.parse_obj(
        {'balance': 1000.0, 'figi': '<FIGI>'}
    )
    api_client.sandbox_positions_balance_post(body, broker_account_id)
    http_client.request.assert_called_once_with(
        'POST',
        '/sandbox/positions/balance',
        response_model=Empty,
        params={'brokerAccountId': broker_account_id},
        data=body.json(by_alias=True),
    )


def test_sandbox_positions_balance_without_broker_account_id(api_client, http_client):
    body = SandboxSetPositionBalanceRequest.parse_obj(
        {'balance': 1000.0, 'figi': '<FIGI>'}
    )
    api_client.sandbox_positions_balance_post(body)
    http_client.request.assert_called_once_with(
        'POST',
        '/sandbox/positions/balance',
        response_model=Empty,
        params={},
        data=body.json(by_alias=True),
    )


def test_sandbox_remove(api_client, http_client, broker_account_id):
    api_client.sandbox_remove_post(broker_account_id)
    http_client.request.assert_called_once_with(
        'POST',
        '/sandbox/remove',
        response_model=Empty,
        params={'brokerAccountId': broker_account_id},
    )


def test_sandbox_remove_without_broker_account_id(api_client, http_client):
    api_client.sandbox_remove_post()
    http_client.request.assert_called_once_with(
        'POST',
        '/sandbox/remove',
        response_model=Empty,
        params={},
    )


def test_sandbox_clear(api_client, http_client, broker_account_id):
    api_client.sandbox_clear_post(broker_account_id)
    http_client.request.assert_called_once_with(
        'POST',
        '/sandbox/clear',
        response_model=Empty,
        params={'brokerAccountId': broker_account_id},
    )


def test_sandbox_clear_without_broker_account_id(api_client, http_client):
    api_client.sandbox_clear_post()
    http_client.request.assert_called_once_with(
        'POST',
        '/sandbox/clear',
        response_model=Empty,
        params={},
    )
