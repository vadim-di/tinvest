# pylint:disable=redefined-outer-name
import pytest

from tinvest import PortfolioApi, PortfolioCurrenciesResponse, PortfolioResponse


@pytest.fixture()
def api_client(http_client):
    return PortfolioApi(http_client)


def test_portfolio_get(api_client, http_client, broker_account_id):
    api_client.portfolio_get(broker_account_id)
    http_client.request.assert_called_once_with(
        'GET',
        '/portfolio',
        response_model=PortfolioResponse,
        params={'brokerAccountId': broker_account_id},
    )


def test_portfolio_get_without_broker_account_id(api_client, http_client):
    api_client.portfolio_get()
    http_client.request.assert_called_once_with(
        'GET',
        '/portfolio',
        response_model=PortfolioResponse,
        params={},
    )


def test_portfolio_currencies_get(api_client, http_client, broker_account_id):
    api_client.portfolio_currencies_get(broker_account_id)
    http_client.request.assert_called_once_with(
        'GET',
        '/portfolio/currencies',
        response_model=PortfolioCurrenciesResponse,
        params={'brokerAccountId': broker_account_id},
    )


def test_portfolio_currencies_get_without_broker_account_id(api_client, http_client):
    api_client.portfolio_currencies_get()
    http_client.request.assert_called_once_with(
        'GET',
        '/portfolio/currencies',
        response_model=PortfolioCurrenciesResponse,
        params={},
    )
