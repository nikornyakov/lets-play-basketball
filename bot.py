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

def send_poll():
    """Функция отправки опроса в канал"""
    try:
        # Получаем токен из переменных окружения
        token = os.getenv("BOT_TOKEN")
        channel_id = os.getenv("CHANNEL_ID")
        
        if not token or not channel_id:
            logger.error("Не установлены BOT_TOKEN или CHANNEL_ID")
            return
        
        # Создаем updater
        updater = Updater(token)
        
        # Определяем текущий день недели
        now = datetime.now()
        day_of_week = now.weekday()  # 4 - пятница
        
        # Форматируем дату для отображения
        date_str = now.strftime("%d.%m.%Y")
        
        if day_of_week == 4:  # Пятница (0-пн, 1-вт, 2-ср, 3-чт, 4-пт, 5-сб, 6-вс)
            question = f"Баскетбол в Четверг ({date_str}) 🏀"
            options = ["✅ Буду", "❌ Не смогу", "🤔 Еще не знаю"]
            message = "Тренировка в Четверг в 19:00. Кто будет?"
            
            # Отправляем опрос
            updater.bot.send_poll(
                chat_id=channel_id,
                question=question,
                options=options,
                is_anonymous=False,
                allows_multiple_answers=False
            )
            
            # Дополнительное текстовое сообщение
            updater.bot.send_message(
                chat_id=channel_id,
                text=message
            )
            
            logger.info(f"Опрос успешно отправлен в пятницу")
            
        else:
            logger.info(f"Сегодня не пятница ({day_of_week}), опрос не отправляется")
            return
        
    except Exception as e:
        logger.error(f"Ошибка при отправке опроса: {e}")

if __name__ == "__main__":
    send_poll()
