import os
import logging
import asyncio
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError

# Настройка логирования в файл
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_poll.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def send_test_poll_async():
    """Асинхронная функция отправки тестового опроса в группу"""
    try:
        # Получаем токен из переменных окружения
        token = os.getenv("BOT_TOKEN")
        group_id = os.getenv("GROUP_ID")
        
        logger.info(f"Получены переменные: BOT_TOKEN={token[:10]}..., GROUP_ID={group_id}")
        
        if not token or not group_id:
            logger.error("Не установлены BOT_TOKEN или GROUP_ID")
            return False
        
        # Преобразуем group_id в целое число
        try:
            group_id = int(group_id)
        except ValueError:
            logger.error(f"GROUP_ID должен быть числом, получено: {group_id}")
            return False
        
        # Создаем экземпляр бота
        bot = Bot(token=token)
        logger.info("Бот успешно инициализирован")
        
        # Текст для тестового опроса
        question = f"Баскетбол во вторник в 19:00 🏀"
        options = ["✅ Буду", "❌ Не смогу", "🤔 Еще не знаю"]
        message = "Тренировка завтра в 19:00. Не забудьте взять воду и форму!"
        
        # Отправляем НЕанонимный опрос (асинхронно)
        logger.info("Отправляем тестовый опрос в группу")
        await bot.send_poll(
            chat_id=group_id,
            question=question,
            options=options,
            is_anonymous=False,
            allows_multiple_answers=False
        )
        
        # Дополнительное текстовое сообщение (асинхронно)
        logger.info("Отправляем текстовое сообщение в группу")
        await bot.send_message(
            chat_id=group_id,
            text=message
        )
        
        logger.info("Тестовый опрос успешно отправлен")
        return True
        
    except TelegramError as e:
        logger.error(f"Ошибка Telegram API при отправке опроса: {e}")
        return False
    except Exception as e:
        logger.error(f"Неожиданная ошибка при отправке тестового опроса: {e}")
        return False

async def main():
    """Основная асинхронная функция"""
    logger.info("=" * 50)
    logger.info("Запуск тестового опроса")
    logger.info("=" * 50)
    
    success = await send_test_poll_async()
    
    if success:
        logger.info("Тестирование завершено успешно!")
    else:
        logger.error("Тестирование завершено с ошибками!")
    
    logger.info("Завершение работы")
    logger.info("=" * 50)

if __name__ == "__main__":
    # Запускаем асинхронную функцию
    asyncio.run(main())
