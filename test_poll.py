import os
import logging
from datetime import datetime
from telegram import Poll
from telegram.ext import Updater

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def send_test_poll():
    """Функция отправки тестового опроса в группу"""
    try:
        # Получаем токен из переменных окружения
        token = os.getenv("BOT_TOKEN")
        group_id = os.getenv("GROUP_ID")
        
        logger.info(f"Получены переменные: BOT_TOKEN={token[:10]}..., GROUP_ID={group_id}")
        
        if not token or not group_id:
            logger.error("Не установлены BOT_TOKEN или GROUP_ID")
            return
        
        # Преобразуем group_id в целое число
        try:
            group_id = int(group_id)
        except ValueError:
            logger.error(f"GROUP_ID должен быть числом, получено: {group_id}")
            return
        
        # Создаем updater
        updater = Updater(token)
        logger.info("Updater успешно создан")
        
        # Форматируем дату для отображения
        date_str = datetime.now().strftime("%d.%m.%Y %H:%M")
        
        # Текст для тестового опроса
        question = f"ТЕСТОВЫЙ ОПРОС ({date_str}) 🏀"
        options = ["✅ Буду", "❌ Не смогу", "🤔 Еще не знаю"]
        message = "Это тестовый опрос для проверки работы бота. Если вы видите это сообщение, бот работает корректно!"
        
        # Отправляем НЕанонимный опрос
        logger.info("Отправляем тестовый опрос в группу")
        poll_message = updater.bot.send_poll(
            chat_id=group_id,
            question=question,
            options=options,
            is_anonymous=False,
            allows_multiple_answers=False
        )
        
        # Дополнительное текстовое сообщение
        logger.info("Отправляем текстовое сообщение в группу")
        updater.bot.send_message(
            chat_id=group_id,
            text=message
        )
        
        # Закрепляем опрос в группе (опционально)
        try:
            updater.bot.pin_chat_message(
                chat_id=group_id,
                message_id=poll_message.message_id
            )
            logger.info("Тестовый опрос закреплен в группе")
        except Exception as e:
            logger.warning(f"Не удалось закрепить опрос: {e}")
        
        logger.info("Тестовый опрос успешно отправлен")
        
    except Exception as e:
        logger.error(f"Ошибка при отправке тестового опроса: {e}")

if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("Запуск тестового опроса")
    logger.info("=" * 50)
    send_test_poll()
    logger.info("Завершение работы")
    logger.info("=" * 50)
