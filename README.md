# T-Invest

[![Build Status](https://api.travis-ci.com/daxartio/tinvest.svg?branch=master)](https://travis-ci.com/daxartio/tinvest)
[![PyPI](https://img.shields.io/pypi/v/tinvest)](https://pypi.org/project/tinvest/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tinvest)](https://www.python.org/downloads/)
[![Codecov](https://img.shields.io/codecov/c/github/daxartio/tinvest)](https://travis-ci.com/daxartio/tinvest)
[![GitHub last commit](https://img.shields.io/github/last-commit/daxartio/tinvest)](https://github.com/daxartio/tinvest)
[![Tinvest](https://img.shields.io/github/stars/daxartio/tinvest?style=social)](https://github.com/daxartio/tinvest)

```
pip install tinvest
```

Данный проект представляет собой инструментарий на языке Python для работы с OpenAPI Тинькофф Инвестиции, который можно использовать для создания торговых роботов.

Клиент предоставляет синхронный и асинхронный API для взаимодействия с Тинькофф Инвестиции.

CLI

```
pip install tinvest[cli]
```

Есть возможность делать запросы через командную строку, подробнее [тут](https://daxartio.github.io/tinvest/cli/).

## Начало работы

### Где взять токен аутентификации?

В разделе инвестиций вашего [личного кабинета tinkoff](https://www.tinkoff.ru/invest/). Далее:

* Перейдите в настройки
* Проверьте, что функция "Подтверждение сделок кодом" отключена
* Выпустите токен для торговли на бирже и режима "песочницы" (sandbox)
* Скопируйте токен и сохраните, токен отображается только один раз, просмотреть его позже не получится, тем не менее вы можете выпускать неограниченное количество токенов

## Документация

[tinvest](https://daxartio.github.io/tinvest/)

[invest-openapi](https://tinkoffcreditsystems.github.io/invest-openapi/)

### Быстрый старт

Для непосредственного взаимодействия с OpenAPI нужно создать клиента. Клиенты разделены на streaming и rest.

Примеры использования SDK находятся ниже.

### У меня есть вопрос

[Основной репозиторий с документацией](https://github.com/TinkoffCreditSystems/invest-openapi/) — в нем вы можете задать вопрос в Issues и получать информацию о релизах в Releases.
Если возникают вопросы по данному SDK, нашёлся баг или есть предложения по улучшению, то можно задать его в Issues.

## Примеры

Для работы с данным пакетом вам нужно изучить [OpenAPI Тинькофф Инвестиции](https://tinkoffcreditsystems.github.io/invest-openapi/swagger-ui/)

### Streaming

В основном, предоставляет асинхронный интерфейс,
но также могут использоваться синхронные хендлеры.
Синхронные хендлеры будут запущены в тредпуле.
Синхронные хендлеры могут быть использованы для работы с синхронными библиотеками,
у которых нет асинхронный реализации.

Все хендлеры в рамках одного типа события будут запущены конкурентно.
Следующее полученное событие будет обрабатываться после успешной обработки предыдущего.
Если у вас планируется долгая обработка, выполняйте её в отдельной таске или процессе.

Если вам требуется время сервера, то можете указать принимаемый аргумент в хендлере под именем `server_time`.
В хендлер будет передано серверное время в формате `datetime`.

> При сетевых сбоях будет произведена попытка переподключения.

```python
import asyncio
from datetime import datetime

import tinvest

TOKEN = "<TOKEN>"

events = tinvest.StreamingEvents()


@events.reconnect()
def handle_reconnect():
    print('Reconnecting')


@events.candle()
async def handle_candle(
    api: tinvest.StreamingApi,
    payload: tinvest.CandleStreaming,
    server_time: datetime  # [optional] if you want
):
    print(payload)


@events.orderbook()
async def handle_orderbook(
    api: tinvest.StreamingApi, payload: tinvest.OrderbookStreaming
):
    print(payload)


@events.instrument_info()
async def handle_instrument_info(
    api: tinvest.StreamingApi, payload: tinvest.InstrumentInfoStreaming
):
    print(payload)


@events.error()
async def handle_error(
    api: tinvest.StreamingApi, payload: tinvest.ErrorStreaming
):
    print(payload)


@events.startup()
async def startup(api: tinvest.StreamingApi):
    await api.candle.subscribe("BBG0013HGFT4", tinvest.CandleResolution.min1)
    await api.orderbook.subscribe("BBG0013HGFT4", 5, "123ASD1123")
    await api.instrument_info.subscribe("BBG0013HGFT4")


@events.cleanup()
async def cleanup(api: tinvest.StreamingApi):
    await api.candle.unsubscribe("BBG0013HGFT4", "1min")
    await api.orderbook.unsubscribe("BBG0013HGFT4", 5)
    await api.instrument_info.unsubscribe("BBG0013HGFT4")


async def main():
    await tinvest.Streaming(TOKEN, state={"postgres": ...}).add_handlers(events).run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

```

### Синхронный REST API Client

Для выполнения синхронных http запросов используется библиотека `requests`.
С описанием клиентов можно ознакомиться по этой [ссылке](https://daxartio.github.io/tinvest/tinvest/apis/).
Возвращаемый аргумент это типичный объект класса `requests.Response`,
который имеет методы `parse_json` и `parse_error`.
Эти методы возвращают объекты, наследованные от класса `pydantic.BaseModel`.

```python
import tinvest

TOKEN = "<TOKEN>"

client = tinvest.SyncClient(TOKEN)
api = tinvest.PortfolioApi(client)

response = api.portfolio_get()  # requests.Response
if response.status_code == 200:
    print(response.parse_json())  # tinvest.PortfolioResponse
```

```python
# Handle error
...
api = tinvest.OperationsApi(client)

response = api.operations_get("", "")
if response.status_code != 200:
    print(response.parse_error())  # tinvest.Error
```

### Асинхронный REST API Client

Для выполнения асинхронных http запросов используется библиотека `aiohttp`.
Клиенты имеют такой же интерфейс как в синхронной реализации, за исключением того,
что функции возвращают объект корутина.

```python
import asyncio
import tinvest

TOKEN = "<TOKEN>"


async def main():
    client = tinvest.AsyncClient(TOKEN)
    api = tinvest.PortfolioApi(client)
    async with api.portfolio_get() as response:  # aiohttp.ClientResponse
        if response.status == 200:
            print(await response.parse_json())  # tinvest.PortfolioResponse

    await client.close()

asyncio.run(main())
```

### Sandbox

Sandbox позволяет вам попробовать свои торговые стратегии, при этом не тратя реальные средства. Протокол взаимодействия полностью совпадает с Production окружением.

```python
client = tinvest.AsyncClient(SANDBOX_TOKEN, use_sandbox=True)
# client = tinvest.SyncClient(SANDBOX_TOKEN, use_sandbox=True)

api = tinvest.SandboxApi(client)
```

## Contributing

Предлагайте свои пулл реквесты, проект с открытым исходным кодом.
