# pylint:disable=too-many-lines
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field

__all__ = (
    'BrokerAccountType',
    'Candle',
    'CandleResolution',
    'Candles',
    'CandlesResponse',
    'Currencies',
    'Currency',
    'CurrencyPosition',
    'Empty',
    'Error',
    'InstrumentType',
    'LimitOrderRequest',
    'LimitOrderResponse',
    'MarketInstrument',
    'MarketInstrumentList',
    'MarketInstrumentListResponse',
    'MarketInstrumentResponse',
    'MarketOrderRequest',
    'MarketOrderResponse',
    'MoneyAmount',
    'Operation',
    'OperationStatus',
    'OperationTrade',
    'OperationType',
    'OperationTypeWithCommission',
    'Operations',
    'OperationsResponse',
    'Order',
    'OrderResponse',
    'OrderStatus',
    'OrderType',
    'Orderbook',
    'OrderbookResponse',
    'OrdersResponse',
    'PlacedLimitOrder',
    'Portfolio',
    'PortfolioCurrenciesResponse',
    'PortfolioPosition',
    'PortfolioResponse',
    'PlacedMarketOrder',
    'SandboxAccount',
    'SandboxCurrency',
    'SandboxSetCurrencyBalanceRequest',
    'SandboxSetPositionBalanceRequest',
    'SandboxRegisterRequest',
    'SandboxRegisterResponse',
    'SearchMarketInstrument',
    'SearchMarketInstrumentResponse',
    'TradeStatus',
    'UserAccount',
    'UserAccounts',
    'UserAccountsResponse',
    'InstrumentInfoStreaming',
    'OrderbookStreaming',
    'ErrorStreaming',
    'CandleStreaming',
    'EventName',
    'ServiceEventName',
)


class BrokerAccountType(str, Enum):
    tinkoff = 'Tinkoff'
    tinkoff_iis = 'TinkoffIis'


class CandleResolution(str, Enum):
    min1 = '1min'
    min2 = '2min'
    min3 = '3min'
    min5 = '5min'
    min10 = '10min'
    min15 = '15min'
    min30 = '30min'
    hour = 'hour'
    day = 'day'
    week = 'week'
    month = 'month'


class Currency(str, Enum):
    rub = 'RUB'
    usd = 'USD'
    eur = 'EUR'
    gbp = 'GBP'
    hkd = 'HKD'
    chf = 'CHF'
    jpy = 'JPY'
    cny = 'CNY'
    try_ = 'TRY'


class InstrumentType(str, Enum):
    stock = 'Stock'
    currency = 'Currency'
    bond = 'Bond'
    etf = 'Etf'


class OperationStatus(str, Enum):
    done = 'Done'
    decline = 'Decline'
    progress = 'Progress'


class OperationType(str, Enum):
    buy = 'Buy'
    sell = 'Sell'


class OperationTypeWithCommission(str, Enum):
    buy = 'Buy'
    buy_card = 'BuyCard'
    sell = 'Sell'
    broker_commission = 'BrokerCommission'
    exchange_commission = 'ExchangeCommission'
    service_commission = 'ServiceCommission'
    margin_commission = 'MarginCommission'
    other_commission = 'OtherCommission'
    pay_in = 'PayIn'
    pay_out = 'PayOut'
    tax = 'Tax'
    tax_lucre = 'TaxLucre'
    tax_dividend = 'TaxDividend'
    tax_coupon = 'TaxCoupon'
    tax_back = 'TaxBack'
    repayment = 'Repayment'
    part_repayment = 'PartRepayment'
    coupon = 'Coupon'
    dividend = 'Dividend'
    security_in = 'SecurityIn'
    security_out = 'SecurityOut'


class OrderStatus(str, Enum):
    new = 'New'
    partially_fill = 'PartiallyFill'
    fill = 'Fill'
    cancelled = 'Cancelled'
    replaced = 'Replaced'
    pending_cancel = 'PendingCancel'
    rejected = 'Rejected'
    pending_replace = 'PendingReplace'
    pending_new = 'PendingNew'


class OrderType(str, Enum):
    limit = 'Limit'
    market = 'Market'


class SandboxCurrency(str, Enum):
    rub = 'RUB'
    usd = 'USD'
    eur = 'EUR'
    gbp = 'GBP'
    hkd = 'HKD'
    chf = 'CHF'
    jpy = 'JPY'
    cny = 'CNY'
    try_ = 'TRY'


class TradeStatus(str, Enum):
    normal_trading = 'NormalTrading'
    not_available_for_trading = 'NotAvailableForTrading'


class MoneyAmount(BaseModel):
    """MoneyAmount"""

    currency: Currency
    value: float


class SearchMarketInstrument(BaseModel):
    currency: Optional[Currency]
    figi: str
    isin: Optional[str]
    lot: int
    min_price_increment: Optional[float] = Field(alias='minPriceIncrement')
    name: str
    ticker: str
    type: InstrumentType


class SearchMarketInstrumentResponse(BaseModel):
    payload: SearchMarketInstrument
    status: str = 'Ok'
    tracking_id: str = Field(alias='trackingId')


class MarketInstrument(BaseModel):
    currency: Optional[Currency]
    figi: str
    isin: Optional[str]
    lot: int
    min_price_increment: Optional[float] = Field(alias='minPriceIncrement')
    name: str
    ticker: str
    type: InstrumentType
    min_quantity: Optional[int] = Field(alias='minQuantity')


class OrderResponse(BaseModel):
    price: float
    quantity: int


class Candle(BaseModel):
    c: float
    figi: str
    h: float
    interval: CandleResolution
    l: float
    o: float
    time: datetime
    v: int


class CurrencyPosition(BaseModel):
    balance: float
    blocked: Optional[float]
    currency: Currency


class Candles(BaseModel):
    candles: List[Candle]
    figi: str
    interval: CandleResolution


class Currencies(BaseModel):
    currencies: List[CurrencyPosition]


class MarketInstrumentList(BaseModel):
    instruments: List[MarketInstrument]
    total: float


class OperationTrade(BaseModel):
    date: datetime
    price: float
    quantity: int
    trade_id: str = Field(alias='tradeId')


class Operation(BaseModel):
    commission: Optional[MoneyAmount]
    currency: Currency
    date: datetime
    figi: Optional[str]
    id: str
    instrument_type: Optional[InstrumentType] = Field(alias='instrumentType')
    is_margin_call: bool = Field(alias='isMarginCall')
    operation_type: Optional[OperationTypeWithCommission] = Field(alias='operationType')
    payment: float
    price: Optional[float]
    quantity: Optional[int]
    quantity_executed: Optional[int] = Field(alias='quantityExecuted')
    status: OperationStatus
    trades: Optional[List[OperationTrade]]


class Operations(BaseModel):
    operations: List[Operation]


class Order(BaseModel):
    executed_lots: int = Field(alias='executedLots')
    figi: str
    operation: OperationType
    order_id: str = Field(alias='orderId')
    price: float
    requested_lots: int = Field(alias='requestedLots')
    status: OrderStatus
    type_: OrderType = Field(alias='type')


class Orderbook(BaseModel):
    asks: List[OrderResponse]
    bids: List[OrderResponse]
    close_price: Optional[float] = Field(alias='closePrice')
    depth: int
    figi: str
    last_price: Optional[float] = Field(alias='lastPrice')
    limit_down: Optional[float] = Field(alias='limitDown')
    limit_up: Optional[float] = Field(alias='limitUp')
    min_price_increment: float = Field(alias='minPriceIncrement')
    face_value: Optional[float] = Field(alias='faceValue')
    trade_status: TradeStatus = Field(alias='tradeStatus')


class PlacedLimitOrder(BaseModel):
    commission: Optional[MoneyAmount]
    executed_lots: int = Field(alias='executedLots')
    operation: OperationType
    order_id: str = Field(alias='orderId')
    reject_reason: Optional[str] = Field(alias='rejectReason')
    message: Optional[str]
    requested_lots: int = Field(alias='requestedLots')
    status: OrderStatus


class PortfolioPosition(BaseModel):
    name: str
    average_position_price: Optional[MoneyAmount] = Field(alias='averagePositionPrice')
    average_position_price_no_nkd: Optional[MoneyAmount] = Field(
        alias='averagePositionPriceNoNkd'
    )
    balance: float
    blocked: Optional[float]
    expected_yield: Optional[MoneyAmount] = Field(alias='expectedYield')
    figi: str
    instrument_type: InstrumentType = Field(alias='instrumentType')
    isin: Optional[str]
    lots: int
    ticker: Optional[str]


class Portfolio(BaseModel):
    positions: List[PortfolioPosition]


class CandlesResponse(BaseModel):
    payload: Candles
    status: str = 'Ok'
    tracking_id: str = Field(alias='trackingId')


class Empty(BaseModel):
    payload: Dict[str, Any]
    status: str = 'Ok'
    tracking_id: str = Field(alias='trackingId')


class Error(BaseModel):
    payload: Dict[str, Any]
    status: str = 'Error'
    tracking_id: str = Field(alias='trackingId')


class LimitOrderRequest(BaseModel):
    lots: int
    operation: OperationType
    price: float


class LimitOrderResponse(BaseModel):
    payload: PlacedLimitOrder
    status: str = 'Ok'
    tracking_id: str = Field(alias='trackingId')


class MarketInstrumentListResponse(BaseModel):
    payload: MarketInstrumentList
    status: str = 'Ok'
    tracking_id: str = Field(alias='trackingId')


class MarketInstrumentResponse(BaseModel):
    payload: MarketInstrument
    status: str = 'Ok'
    tracking_id: str = Field(alias='trackingId')


class MarketOrderRequest(BaseModel):
    lots: int
    operation: OperationType


class PlacedMarketOrder(BaseModel):
    order_id: str = Field(alias='orderId')
    operation: OperationType
    status: OrderStatus
    reject_reason: Optional[str] = Field(alias='rejectReason')
    message: Optional[str]
    requested_lots: int = Field(alias='requestedLots')
    executed_lots: int = Field(alias='executedLots')
    commission: Optional[MoneyAmount]


class MarketOrderResponse(BaseModel):
    payload: PlacedMarketOrder
    status: str = 'Ok'
    tracking_id: str = Field(alias='trackingId')


class OperationsResponse(BaseModel):
    payload: Operations
    status: str = 'Ok'
    tracking_id: str = Field(alias='trackingId')


class OrderbookResponse(BaseModel):
    payload: Orderbook
    status: str = 'Ok'
    tracking_id: str = Field(alias='trackingId')


class OrdersResponse(BaseModel):
    payload: List[Order]
    status: str = 'Ok'
    tracking_id: str = Field(alias='trackingId')


class PortfolioCurrenciesResponse(BaseModel):
    payload: Currencies
    status: str = 'Ok'
    tracking_id: str = Field(alias='trackingId')


class PortfolioResponse(BaseModel):
    payload: Portfolio
    status: str = 'Ok'
    tracking_id: str = Field(alias='trackingId')


class SandboxSetCurrencyBalanceRequest(BaseModel):
    balance: float
    currency: SandboxCurrency


class SandboxSetPositionBalanceRequest(BaseModel):
    balance: float
    figi: Optional[str]


class SandboxAccount(BaseModel):
    broker_account_type: BrokerAccountType = Field(alias='brokerAccountType')
    broker_account_id: str = Field(alias='brokerAccountId')


class SandboxRegisterResponse(BaseModel):
    tracking_id: str = Field(alias='trackingId')
    status: str
    payload: SandboxAccount


class SandboxRegisterRequest(BaseModel):
    broker_account_type: BrokerAccountType = Field(alias='brokerAccountType')

    class Config:
        allow_population_by_field_name = True


class UserAccount(BaseModel):
    broker_account_type: BrokerAccountType = Field(alias='brokerAccountType')
    broker_account_id: str = Field(alias='brokerAccountId')


class UserAccounts(BaseModel):
    accounts: List[UserAccount]


class UserAccountsResponse(BaseModel):
    tracking_id: str = Field(alias='trackingId')
    status: str
    payload: UserAccounts


class InstrumentInfoStreaming(BaseModel):
    figi: str
    trade_status: str
    min_price_increment: float
    lot: float
    accrued_interest: Optional[float]
    limit_up: Optional[float]
    limit_down: Optional[float]


class OrderbookStreaming(BaseModel):
    figi: str
    depth: int
    bids: List[Tuple[float, float]]
    asks: List[Tuple[float, float]]


class ErrorStreaming(BaseModel):
    error: str
    request_id: Optional[str]


CandleStreaming = Candle


class EventName(str, Enum):
    candle = 'candle'
    orderbook = 'orderbook'
    instrument_info = 'instrument_info'
    error = 'error'


class ServiceEventName(str, Enum):
    startup = 'startup'
    cleanup = 'cleanup'
    reconnect = 'reconnect'
