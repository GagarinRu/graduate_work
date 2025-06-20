import logging

from aio_pika.exceptions import AMQPConnectionError, ChannelClosed, ConnectionClosed
from faststream.rabbit import RabbitExchange, RabbitQueue
from pydantic import BaseModel
from src.utils.backoff import backoff

from .broker import broker

logger = logging.getLogger(__name__)


@backoff(expected_exceptions=(AMQPConnectionError, ConnectionClosed, ChannelClosed))
async def publish(message: BaseModel, queue: RabbitQueue, exchange: RabbitExchange = None):
    try:
        await broker.publish(message, queue=queue, exchange=exchange)
        logger.info(f"Сообщение успешно опубликовано в очередь: {queue.name}, exchange: {exchange.name}")
    except Exception as e:
        logger.error(f"Ошибка при публикации сообщения: {e}")
