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
        day_of_week = now.weekday()  # 0 - понедельник, 2 - среда
        
        # Форматируем дату для отображения
        date_str = now.strftime("%d.%m.%Y")
        
        if day_of_week == 0:  # Понедельник
            question = f"Баскетбол в понедельник ({date_str}) 🏀"
            options = ["✅ Буду", "❌ Не смогу", "🤔 Еще не знаю"]
            message = "Завтра тренировка в 19:00. Кто будет?"
            
        elif day_of_week == 2:  # Среда
            question = f"Баскетбол в среду ({date_str}) 🏀"
            options = ["✅ Буду", "❌ Не смогу", "🤔 Еще не знаю"]
            message = "Завтра тренировка в 19:00. Кто будет?"
            
        else:
            logger.info("Сегодня не понедельник и не среда, опрос не отправляется")
            return
        
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
        
        logger.info(f"Опрос успешно отправлен для дня недели: {day_of_week}")
        
    except Exception as e:
        logger.error(f"Ошибка при отправке опроса: {e}")

if __name__ == "__main__":
    send_poll()
