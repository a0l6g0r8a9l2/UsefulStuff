import asyncio
import logging
from functools import partial
from typing import List

import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.logging import setup_logging

setup_logging(default_level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def check(ticker, exchange_url_suffix):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}{exchange_url_suffix}?modules=price')
        price = r.json()["quoteSummary"]["result"][0]["price"]["regularMarketPrice"]["raw"]
    logger.info(f'{ticker} - price: {price}')


async def check_all_me(exchange_url_suffix: str, tickers: List[str]):
    [await check(t, exchange_url_suffix) for t in tickers]


async def check_all_ne(exchange_url_suffix: str, tickers: List[str]):
    [await check(t, exchange_url_suffix) for t in tickers]


async def main():
    scheduler = AsyncIOScheduler()
    _check_all_me = partial(check_all_me, exchange_url_suffix='.ME', tickers=['ALRS', 'MOEX', 'SBER', 'YNDX'])
    _check_all_ne = partial(check_all_ne, exchange_url_suffix='', tickers=['CCL', 'O', 'T', 'KO'])
    scheduler.add_job(_check_all_me, 'interval', seconds=5, id='1', name='scheduler for ME tickers')
    scheduler.add_job(_check_all_ne, 'interval', seconds=3, id='2', name='scheduler for all other')
    scheduler.start()


try:
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
except (KeyboardInterrupt, SystemExit):
    pass
