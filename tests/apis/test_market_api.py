# pylint:disable=redefined-outer-name
from datetime import datetime, timedelta

import pytest

from tinvest import (
    CandleResolution,
    CandlesResponse,
    MarketApi,
    MarketInstrumentListResponse,
    OrderbookResponse,
    SearchMarketInstrumentResponse,
)


@pytest.fixture()
def api_client(http_client):
    return MarketApi(http_client)


def test_market_stocks_get(api_client, http_client):
    api_client.market_stocks_get()
    http_client.request.assert_called_once_with(
        'GET', '/market/stocks', response_model=MarketInstrumentListResponse
    )


def test_market_bonds_get(api_client, http_client):
    api_client.market_bonds_get()
    http_client.request.assert_called_once_with(
        'GET',
        '/market/bonds',
        response_model=MarketInstrumentListResponse,
    )


def test_market_etfs_get(api_client, http_client):
    api_client.market_etfs_get()
    http_client.request.assert_called_once_with(
        'GET',
        '/market/etfs',
        response_model=MarketInstrumentListResponse,
    )


def test_market_currencies_get(api_client, http_client):
    api_client.market_currencies_get()
    http_client.request.assert_called_once_with(
        'GET',
        '/market/currencies',
        response_model=MarketInstrumentListResponse,
    )


def test_market_orderbook_get(api_client, http_client, figi):
    api_client.market_orderbook_get(figi, 2)
    http_client.request.assert_called_once_with(
        'GET',
        '/market/orderbook',
        response_model=OrderbookResponse,
        params={'figi': figi, 'depth': 2},
    )


def test_market_candles_get(api_client, http_client, figi):
    to = datetime.now()
    from_ = to - timedelta(days=7)
    api_client.market_candles_get(
        figi, from_.isoformat(), to.isoformat(), CandleResolution.min1
    )
    http_client.request.assert_called_once_with(
        'GET',
        '/market/candles',
        response_model=CandlesResponse,
        params={
            'figi': figi,
            'from': from_.isoformat(),
            'to': to.isoformat(),
            'interval': CandleResolution.min1,
        },
    )


def test_market_search_by_figi_get(api_client, http_client, figi):
    api_client.market_search_by_figi_get(figi)
    http_client.request.assert_called_once_with(
        'GET',
        '/market/search/by-figi',
        response_model=SearchMarketInstrumentResponse,
        params={'figi': figi},
    )


def test_market_search_by_ticker_get(api_client, http_client):
    ticker = 'some_ticker'
    api_client.market_search_by_ticker_get(ticker)
    http_client.request.assert_called_once_with(
        'GET',
        '/market/search/by-ticker',
        response_model=MarketInstrumentListResponse,
        params={'ticker': ticker},
    )
