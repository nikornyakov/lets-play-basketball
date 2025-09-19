import os
import logging
from datetime import datetime
from telegram import Poll
from telegram.ext import Updater

# Создаем папку для логов, если она не существует
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Настройка логирования
log_file = os.path.join(log_dir, f"bot_{datetime.now().strftime('%Y%m%d')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def send_poll():
    """Функция отправки опроса в закрытую группу"""
    try:
        logger.info("Запуск функции отправки опроса в закрытую группу")
        
        # Получаем токен из переменных окружения
        token = os.getenv("BOT_TOKEN")
        group_id = os.getenv("GROUP_ID")  # ID закрытой группы (отрицательное число)
        
        logger.info(f"Получены переменные: BOT_TOKEN={token[:10]}..., GROUP_ID={group_id}")
        
        if not token or not group_id:
            logger.error("Не установлены BOT_TOKEN или GROUP_ID")
            return
        
        # Преобразуем group_id в целое число (если оно передано как строка)
        try:
            group_id = int(group_id)
        except ValueError:
            logger.error(f"GROUP_ID должен быть числом, получено: {group_id}")
            return
        
        # Создаем updater
        updater = Updater(token)
        logger.info("Updater успешно создан")
        
        # Определяем текущий день недели
        now = datetime.now()
        day_of_week = now.weekday()
        day_name = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"][day_of_week]
        
        logger.info(f"Текущий день: {day_name} ({day_of_week})")
        
        # Форматируем дату для отображения
        date_str = now.strftime("%d.%m.%Y")
        
        if day_of_week == 0:  # Понедельник
            logger.info("Определен понедельник, готовим опрос")
            question = f"Баскетбол в вторник ({date_str}) 🏀"
            options = ["✅ Буду", "❌ Не смогу", "🤔 Еще не знаю"]
            message = "Тренировка завтра в 19:00. Не забудьте взять воду и форму!"
            
        elif day_of_week == 2:  # Среда
            logger.info("Определена среда, готовим опрос")
            question = f"Баскетбол в четверг ({date_str}) 🏀"
            options = ["✅ Буду", "❌ Не смогу", "🤔 Еще не знаю"]
            message = "Тренировка завтра в 19:00. Не забудьте взять воду и форму!"
            
        else:
            logger.info(f"Сегодня {day_name}, опрос не требуется")
            return
        
        # Отправляем НЕанонимный опрос в закрытую группу
        logger.info("Отправляем неанонимный опрос в закрытую группу")
        poll_message = updater.bot.send_poll(
            chat_id=group_id,
            question=question,
            options=options,
            is_anonymous=False,  # Неанонимный опрос
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
            logger.info("Опрос закреплен в группе")
        except Exception as e:
            logger.warning(f"Не удалось закрепить опрос: {e}")
        
        logger.info(f"Неанонимный опрос успешно отправлен в {day_name}")
        
    except Exception as e:
        logger.error(f"Ошибка при отправке опроса: {e}", exc_info=True)

if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("Запуск бота для отправки опроса в закрытую группу")
    logger.info("=" * 50)
    send_poll()
    logger.info("Завершение работы бота")
    logger.info("=" * 50)
